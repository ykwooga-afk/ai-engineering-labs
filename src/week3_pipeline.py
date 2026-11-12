"""Week 3 V1 data pipeline: ingest, inspect, prepare, validate, store, lineage.

No fitted preprocessing, split, model, retrieval index or external model API.
Both branches read raw inputs anew on each call and use explicit configuration.
"""
from pathlib import Path
from datetime import datetime, timezone
from tempfile import TemporaryDirectory
import hashlib
import json
import os
import platform
import re
import unicodedata
import pandas as pd
import pypdf
from pypdf import PdfReader

PIPELINE_VERSION = 'week3-v1'

def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def json_write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n', encoding='utf-8')

def clean_page(text):
    text = unicodedata.normalize('NFC', text)
    for old,new in {'ﬀ':'ff','ﬁ':'fi','ﬂ':'fl','ﬃ':'ffi','ﬄ':'ffl'}.items():
        text = text.replace(old,new)
    text = text.replace('\r\n','\n').replace('\r','\n')
    lines = []
    for line in text.split('\n'):
        line = re.sub(r'[ \t]+', ' ', line).strip()
        if re.fullmatch(r'(Data 2022, 7, (?:146|x FOR PEER REVIEW)|Appl\. Sci\. 2023, 13, 4702)\s+\d+ of \d+', line):
            continue
        lines.append(line)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()

def page_spans(text, size=1000):
    if size <= 0:
        raise ValueError('Chunk size must be positive')
    start = 0
    while start < len(text):
        while start < len(text) and text[start].isspace(): start += 1
        if start == len(text): break
        end = min(start+size, len(text))
        if end < len(text):
            lower = start + size//2
            for marker in ['\n\n', '\n', ' ']:
                pos = text.rfind(marker, lower, end)
                if pos >= lower:
                    end = pos+len(marker)
                    break
        stop = end
        while stop > start and text[stop-1].isspace(): stop -= 1
        yield start, stop
        start = end

def require(condition, message):
    if not bool(condition):
        raise ValueError(message)

def ingest(base_dir, source_ids, registry):
    """Missing files or changed source bytes stop before any output is written."""
    sources = []
    for sid in source_ids:
        source = registry[sid]
        path = Path(base_dir)/'data/raw'/source['filename']
        if not path.is_file():
            raise FileNotFoundError(f'{sid}: missing input {source["filename"]}')
        digest = file_hash(path)
        require(digest == source['sha256'], f'{sid}: source checksum mismatch; review the new version')
        sources.append({'source_id':sid, 'path':'data/raw/'+source['filename'],
            'sha256':digest, 'bytes':path.stat().st_size,
            'source_version':source['version'], 'source_url':source['url'],
            'attribution':source['authors'], 'access_rights':source['licence']})
    return sources

def prepare_tabular(base_dir, staging, cfg, registry):
    source = Path(base_dir)/'data/raw'/registry['S01']['filename']
    df = pd.read_csv(source, sep=cfg['separator'])
    require(df.shape == (cfg['expected_rows'], len(cfg['expected_raw_columns'])), 'Unexpected table dimensions')
    require(df.columns.tolist() == cfg['expected_raw_columns'], 'Unexpected table schema or column order')
    require(set(df['Target']) == set(cfg['labels']), 'Unexpected target labels')
    info = {'rows':len(df), 'columns':df.shape[1], 'missing_cells':int(df.isna().sum().sum()),
        'exact_duplicate_rows':int(df.duplicated().sum()),
        'class_counts':{str(k):int(v) for k,v in df['Target'].value_counts().items()}}
    clean = df.rename(columns=lambda s:s.strip()).copy()
    require(clean.columns.is_unique, 'Header normalization caused a collision')
    for c in clean.select_dtypes(include=['object','string']).columns:
        clean[c] = clean[c].astype('string').str.strip()
    features = [c for c in clean if c!='Target']
    conflict = clean.groupby(features,dropna=False)['Target'].transform('nunique').gt(1)
    repeated = clean.duplicated(keep='first') & ~conflict
    rejected = conflict | repeated
    keys = pd.Series([f'uci697-{i+1:06d}' for i in range(len(clean))],index=clean.index)
    prepared = clean.loc[~rejected].copy()
    prepared.insert(0,'row_id',keys.loc[prepared.index])
    quarantine = clean.loc[rejected].copy()
    quarantine.insert(0,'row_id',keys.loc[quarantine.index])
    quarantine['reason'] = ['conflicting_labels' if conflict.loc[i] else 'exact_duplicate' for i in quarantine.index]
    require(not prepared.empty,'Preparation removed all records')
    require(len(prepared)+len(quarantine)==len(df),'Row accounting failed')
    require(prepared.row_id.is_unique,'Duplicate row keys')
    require(prepared['Admission grade'].between(0,200).all(),'Admission grade outside 0..200')
    require(prepared['Previous qualification (grade)'].between(0,200).all(),'Previous grade outside 0..200')
    sem1=[c for c in clean if c.startswith('Curricular units 1st sem')]
    require((prepared[[c for c in sem1 if '(grade)' not in c]]>=0).all().all(),'Negative semester-one count')
    require(prepared['Curricular units 1st sem (grade)'].between(0,20).all(),'Semester-one grade outside 0..20')
    forbidden={c for c in clean if '2nd sem' in c} | set(cfg['excluded_timing']) | {'Target','row_id','Gender','Nacionality'}
    for timepoint in ['T0','T1']:
        allowed=cfg[timepoint]
        require(len(allowed)==len(set(allowed)),f'{timepoint}: duplicated feature')
        require(not (set(allowed)&forbidden),f'{timepoint}: prohibited predictor')
        require(set(allowed)<=set(clean.columns),f'{timepoint}: unknown feature')
    require(not any('1st sem' in c for c in cfg['T0']),'T0 contains first-semester information')
    require(cfg['T1']==cfg['T0']+sem1,'T1 does not match the selected Part B policy')
    frames={'prepared_table.csv':prepared, 'quarantined_rows.csv':quarantine,
        'features_t0.csv':prepared[['row_id']+cfg['T0']],
        'features_t1.csv':prepared[['row_id']+cfg['T1']],
        'targets.csv':prepared[['row_id','Target']],
        'audit_attributes.csv':prepared[['row_id']+cfg['audit']]}
    for name,frame in frames.items():
        frame.to_csv(staging/name,index=False,lineterminator='\n')
        actual=pd.read_csv(staging/name)
        pd.testing.assert_frame_equal(actual,frame.reset_index(drop=True),check_dtype=False)
    allowlists={'version':'week3-ab-v1','T0':cfg['T0'],'T1':cfg['T1'],
        'join_key_not_predictor':'row_id','target_file':'targets.csv','audit_file':'audit_attributes.csv'}
    json_write(staging/'feature_allowlists.json',allowlists)
    require(json.loads((staging/'feature_allowlists.json').read_text())==allowlists,'Allowlist round-trip failed')
    outputs=list(frames)+['feature_allowlists.json']
    info.update({'prepared_rows':len(prepared),'quarantined_rows':len(quarantine),
                 't0_features':len(cfg['T0']),'t1_features':len(cfg['T1'])})
    mappings=[{'source_id':'S01','source':'data/raw/'+registry['S01']['filename'],
        'output':'data/pipeline_v1/tabular/'+name,
        'row_mapping':'uci697-{one-based original data-row ordinal:06d}; fixed source hash'} for name in outputs]
    return outputs,mappings,info,[]

def prepare_documents(base_dir, staging, cfg, registry):
    require(cfg['method']=='page-aware-paragraph-line','Unsupported chunking method')
    require(cfg['overlap']==0,'V1 supports zero overlap only')
    size=cfg['chunk_size']
    require(isinstance(size,int) and size>0,'Invalid chunk size')
    chunks,info,warnings=[],[],[]
    for sid in cfg['source_ids']:
        source=registry[sid]
        reader=PdfReader(Path(base_dir)/'data/raw'/source['filename'])
        raw_pages=[p.extract_text() or '' for p in reader.pages]
        require(raw_pages and all(t.strip() for t in raw_pages),f'{sid}: empty page extraction; inspect OCR needs')
        pages=[clean_page(t) for t in raw_pages]
        count_before=len(chunks)
        for page_number,text in enumerate(pages,1):
            flags=['manual_source_check_required']
            raw=raw_pages[page_number-1]
            if len(raw)>10000:flags.append('unusually_dense_extraction')
            if 'FOR PEER REVIEW' in raw:flags.append('peer_review_text_in_extraction')
            if 'Table ' in text:flags.append('possible_table_reading_order_loss')
            if page_number==1:flags.append('publisher_sidebar_retained')
            page_chunks=[]
            for start,end in page_spans(text,size):
                row={'record_id':f"{sid}-{source['sha256'][:12]}-p{page_number:03d}-c{start:06d}",
                    'text':text[start:end],'source_id':sid,'source':'data/raw/'+source['filename'],
                    'source_sha256':source['sha256'],'source_url':source['url'],
                    'source_version':source['version'],'page':page_number,
                    'start_char_in_clean_page':start,'end_char_in_clean_page':end,
                    'processing':f'page-aware paragraph/line-boundary packing; max_chars={size}; overlap=0; minimal-clean-v1',
                    'licence':'CC BY 4.0','status':'candidate_for_manual_review','warnings':flags}
                require(0<len(row['text'].strip())<=size,f'{sid}: empty or oversized chunk')
                page_chunks.append(row)
            require(page_chunks,f'{sid}: no chunks on page {page_number}')
            normal=lambda t:re.sub(r'\s+','',t)
            require(normal(''.join(r['text'] for r in page_chunks))==normal(text),f'{sid}: page coverage loss')
            chunks.extend(page_chunks)
            if len(flags)>1:warnings.append({'source_id':sid,'page':page_number,'warnings':flags[1:]})
        info.append({'source_id':sid,'pages':len(pages),'raw_characters':sum(map(len,raw_pages)),
                     'chunks':len(chunks)-count_before})
    require(len({r['record_id'] for r in chunks})==len(chunks),'Duplicate chunk IDs')
    target=staging/'prepared_text.jsonl'
    with target.open('w',encoding='utf-8') as f:
        for row in chunks:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    restored=[json.loads(line) for line in target.read_text(encoding='utf-8').splitlines() if line.strip()]
    require(restored==chunks,'Document JSONL round-trip mismatch')
    mappings=[{'source_id':sid,'source':'data/raw/'+registry[sid]['filename'],
        'output':'data/pipeline_v1/documents/prepared_text.jsonl',
        'record_selector':{'source_id':sid},'page_range':[1,len(PdfReader(Path(base_dir)/'data/raw'/registry[sid]['filename']).pages)]}
        for sid in cfg['source_ids']]
    return ['prepared_text.jsonl'],mappings,{'documents':info,'total_chunks':len(chunks)},warnings

def verify_saved_run(base_dir,record):
    """Verify hashes on disk, not just a previously printed PASS."""
    base_dir=Path(base_dir)
    for source in record['sources']:
        path=base_dir/source['path']
        require(path.is_file() and file_hash(path)==source['sha256'],'Saved run source fingerprint mismatch')
    require(record['outputs'],'No output records')
    for output in record['outputs']:
        path=base_dir/output['path']
        require(path.is_file() and path.stat().st_size>0,'Missing or empty saved output')
        require(file_hash(path)==output['sha256'] and path.stat().st_size==output['bytes'],'Saved output fingerprint mismatch')
    sources={s['source_id'] for s in record['sources']}
    paths={o['path'] for o in record['outputs']}
    require({m['source_id'] for m in record['source_output_mapping']}==sources,'Source without a lineage mapping')
    require({m['output'] for m in record['source_output_mapping']}==paths,'Output without a lineage mapping')
    for mapping in record['source_output_mapping']:
        expected=next(s['path'] for s in record['sources'] if s['source_id']==mapping['source_id'])
        require(mapping['source']==expected,'Wrong source in mapping')
    return True

def run_pipeline(kind,base_dir,registry,configuration,runtime='Local Python'):
    """Execute a complete branch from raw input without Part B in-memory data."""
    base_dir=Path(base_dir).resolve()
    require(kind in ['tabular','documents'],'Select a supported branch')
    cfg=json.loads(json.dumps(configuration))
    source_ids=['S01'] if kind=='tabular' else cfg['source_ids']
    sources=ingest(base_dir,source_ids,registry)
    out=base_dir/'data/pipeline_v1'/kind
    out.parent.mkdir(parents=True,exist_ok=True)
    with TemporaryDirectory(prefix='week3_staging_',dir=out.parent) as temporary:
        staging=Path(temporary)
        prepare=prepare_tabular if kind=='tabular' else prepare_documents
        names,mappings,inspection,warnings=prepare(base_dir,staging,cfg,registry)
        require(names and len(names)==len(set(names)),'Missing or duplicate output filenames')
        outputs=[]
        for name in names:
            path=staging/name
            require(path.is_file() and path.stat().st_size>0,'Prepared output is missing or empty')
            outputs.append({'path':str((out/name).relative_to(base_dir)),
                'sha256':file_hash(path),'bytes':path.stat().st_size})
        record={'pipeline_version':PIPELINE_VERSION,'generated_at_utc':datetime.now(timezone.utc).isoformat(),
            'data_type':kind,'runtime':runtime,
            'environment':{'python':platform.python_version(),'pandas':pd.__version__,'pypdf':pypdf.__version__},
            'configuration':cfg,'sources':sources,'inspection':inspection,'outputs':outputs,
            'source_output_mapping':mappings,'validation':{'content_roundtrip':'PASS','output_count':len(outputs)},
            'warnings':warnings,'status':'PREPARED; full quality review pending',
            'provenance_limitations':'Hashes identify bytes; they do not prove fairness, guide claim correctness or real-time feature validity.'}
        # Only validated temporary outputs are promoted; manifest is written last.
        out.mkdir(parents=True,exist_ok=True)
        for name in names:os.replace(staging/name,out/name)
        verify_saved_run(base_dir,record)
        json_write(staging/'pipeline_manifest.json',record)
        os.replace(staging/'pipeline_manifest.json',out/'pipeline_manifest.json')
    require(json.loads((out/'pipeline_manifest.json').read_text())==record,'Run manifest round-trip failed')
    print(f'SUCCESS: {kind} | Inputs: {len(sources)} | Outputs: {len(outputs)}')
    print('Manifest:',str((out/'pipeline_manifest.json').relative_to(base_dir)))
    return record

def repeatability_signature(record):
    """Execution timestamp is expected to differ; all deterministic evidence matches."""
    return {k:v for k,v in record.items() if k!='generated_at_utc'}
