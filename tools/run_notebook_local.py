"""Execute this notebook's plain Python cells in order without a Jupyter server.

This is local Python execution, not Google Colab execution. Only use with this
trusted notebook: Python cells are executed as code. Actual stdout/stderr are
stored as notebook stream outputs. No output is fabricated or replayed.
"""
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
import io
import json
import os
import traceback

root = Path(__file__).resolve().parents[1]
path = root / 'notebooks/week3_pipeline.ipynb'
notebook = json.loads(path.read_text(encoding='utf-8'))
os.chdir(root)
namespace = {'__name__': '__main__'}
count = 0
for cell in notebook['cells']:
    if cell['cell_type'] != 'code':
        continue
    count += 1
    cell['execution_count'] = count
    cell['outputs'] = []
    stdout, stderr = io.StringIO(), io.StringIO()
    failure = None
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(compile(''.join(cell['source']), f'notebook_cell_{count}', 'exec'), namespace)
    except Exception as error:
        failure = error
        cell['outputs'].append({'output_type':'error','ename':type(error).__name__,
            'evalue':str(error),'traceback':traceback.format_exc().splitlines()})
    for name, buffer in [('stdout',stdout),('stderr',stderr)]:
        if buffer.getvalue():
            cell['outputs'].append({'output_type':'stream','name':name,'text':buffer.getvalue().splitlines(keepends=True)})
    notebook['metadata']['execution_method'] = 'Local Python sequential exec; actual stdout/stderr captured; not Colab or a Jupyter kernel'
    path.write_text(json.dumps(notebook,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Cell {count}: {"FAIL" if failure else "PASS"}',flush=True)
    if failure:
        raise failure
print(f'Executed {count} cells. Saved actual outputs to {path.name}.')
