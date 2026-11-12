# Week 3 Data Inventory — Part A

**Project:** Explainable Student Dropout Prediction Using Early Academic Indicators
**Student:** Woo Yong Kang | A24AI0123 | SAIA3113 AI Engineering

## A1. Requirement and architecture traceability

| Requirement | Needed information | Source | Architecture / evaluation link |
|---|---|---|---|
| FR2 | Timepoint-specific tabular features and original three-class outcome | S01 | D1 → A7; E1 timing controls |
| FR5 | Source-linked definitions, timing and limits | S02, S03 | D2 → A6; E4 source support |
| NFR4 | Fixed sources and explicit preparation | All | A7/A9; E8 later repeatability |

RAI1 separates audit attributes, RAI2 restricts public row-level output, and RAI4 requires manual guide-claim verification. Model-level acceptance targets remain unevaluated.

## A2–A4. Source inventory

| ID | File / canonical source | Type and purpose | Version / date / owner | Access / rights | Inspection evidence |
|---|---|---|---|---|---|
| S01 | `data/raw/uci_dropout.csv`; [Predict Students' Dropout and Academic Success](https://doi.org/10.24432/C5MC89) | Structured tabular CSV; later tabular prediction; not live student assessment | UCI release retrieved 2026-11-12; identified by SHA-256; accessed 2026-11-12; Realinho, V.; Vieira Martins, M.; Machado, J.; Baptista, L. (2021) | CC BY 4.0 with attribution; no institution login needed | 4,424 rows × 37 columns; 0 missing cells; 0 exact duplicates; two 100-row subsets inspected |
| S02 | `data/raw/realinho_2022.pdf`; [Predicting Student Dropout and Academic Success](https://doi.org/10.3390/data7110146) | Unstructured PDF text; candidate reference-guide evidence, not training labels | Data 7(11), 146; unchanged Lab 2 PDF; accessed 2026-11-05; Realinho, V.; Machado, J.; Baptista, L.; Martins, M. V. (2022) | CC BY 4.0 with attribution; no institution login needed | 17 pages; 99,741 extracted characters; pp.1 and 5 sampled; all pages nonempty |
| S03 | `data/raw/martins_2023.pdf`; [Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education](https://doi.org/10.3390/app13084702) | Unstructured PDF text; candidate reference-guide evidence, not training labels | Applied Sciences 13(8), 4702; unchanged Lab 2 PDF; accessed 2026-11-05; Martins, M. V.; Baptista, L.; Machado, J.; Realinho, V. (2023) | CC BY 4.0 with attribution; no institution login needed | 15 pages; 50,591 extracted characters; pp.1 and 5 sampled; all pages nonempty |

## Observable ingestion evidence

The CSV was explicitly parsed with `sep=";"`. `Daytime/evening attendance` has a trailing tab in the raw header. The published spelling `Nacionality` is retained and documented as nationality.

| Source-order inspection subset | Rows | Missing cells | Class counts | Admission grade min / max |
|---|---:|---:|---|---|
| first_100_source_rows | 100 | 0 | {'Graduate': 49, 'Dropout': 29, 'Enrolled': 22} | 100.0 / 180.4 |
| last_100_source_rows | 100 | 0 | {'Graduate': 49, 'Dropout': 35, 'Enrolled': 16} | 100.0 / 166.0 |

These disjoint subsets are ingestion checks, not train/test partitions. Notebook output and `evidence/table_inspection.json` retain the loaded schema, types and actual aggregate values. `evidence/pdf_inspection.json` retains text samples and page-level warnings.

## Source identity and raw/prepared storage

Raw originals: `data/raw/`. Part B exports: `data/processed/`. Source registry: `data/source_registry.json`. Common Part B lineage: `data/week3_manifest.json`.
In Colab these paths are under `/content/week3_project`; they are temporary. Download generated outputs and save the executed notebook before disconnecting. The private submission ZIP contains the working CSVs. No Google Drive storage is used. See the project README for repository evidence.

| Source | SHA-256 |
|---|---|
| S01 | `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae` |
| S02 | `1be95db77df7714e2b0783811c414895150c45cee6bbd8a79d6bd61b3a2185fb` |
| S03 | `2f092cb9803c2ae1f3a9198f9fe3752c3f664c0f5307b2177417a8c057d4ab46` |

## Rights, scope and quality limitations

- The UCI licence permits attributed reuse, but Week 2 RAI2 is stricter for publication: keep row-level source/prepared tables private and publish aggregate evidence. The included `.gitignore` supports that rule.
- Copyright for both CC BY 4.0 papers remains with the authors. The original PDF bytes are unchanged; derived text carries source URL, version, page and processing description.
- The sources concern Portuguese higher education. They do not establish UTM performance or support real student decisions.
- The 2023 study reports 4,433 records (§4.1, PDF p.4); the actual UCI release has 4,424. Do not silently equate their versions.
- S02 has duplicated/overlapping table extraction and peer-review text. S03 tables lose their layout in plain text. Both include a first-page publisher sidebar. All guide chunks remain candidates for manual checking.
- Model training, embeddings, vector indexing, full Topic 4 quality/fairness assessment are not claimed. Part C follows in the same notebook.

## A4 checkpoint

The data sources are justified by FR2 and FR5, all three pinned files were loaded, and the notebook shows their actual structure/content. One tabular dataset plus two supporting documents is sufficient; the six lab pathways are alternatives.

## Source references

1. Realinho et al. (2021). UCI Predict Students’ Dropout and Academic Success. https://doi.org/10.24432/C5MC89
2. Realinho et al. (2022). Data 7(11), 146. https://doi.org/10.3390/data7110146
3. Martins et al. (2023). Applied Sciences 13(8), 4702. https://doi.org/10.3390/app13084702
4. Existing project requirements: https://github.com/ykwooga-afk/ai-engineering-labs/blob/main/docs/week2_requirements.md
5. Licence: https://creativecommons.org/licenses/by/4.0/
