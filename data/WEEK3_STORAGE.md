# Week 3 Data Access and Storage

The public repository contains source attribution, code, aggregate evidence and fingerprints. The private `Lab3_ABC_WOO_YONG_KANG_A24AI0123.zip` contains the full raw and prepared working files for assessment/local use. No public link to that private archive is required for reproducing the pipeline.

| Artefact | Private working/submission location | Public evidence / recovery |
|---|---|---|
| Raw benchmark | `data/raw/uci_dropout.csv` | Download official UCI DOI 10.24432/C5MC89; notebook extracts `data.csv` from its ZIP and checks SHA-256 |
| Original PDFs | `data/raw/realinho_2022.pdf`, `data/raw/martins_2023.pdf` | Already attributed originals in repository `data/`; notebook copies/downloads their bytes and verifies hashes |
| Part B row-level tables | `data/processed/*.csv` | Recreate from the notebook; hashes in `data/week3_manifest.json` |
| Part C row-level tables | `data/pipeline_v1/tabular/*.csv` | Recreate from raw input; hashes/counts in `pipeline_manifest.json` |
| Document candidates | `data/processed/prepared_text.jsonl`, `data/pipeline_v1/documents/prepared_text.jsonl` | Attributed CC BY-derived text can be stored publicly; all chunks require manual guide-claim review |
| Audit/target records | Separate CSV files within each private preparation directory | Public notebook outputs contain only aggregates and metadata |

In Colab, the project root is `/content/week3_project`. Its files are temporary; save the executed notebook and download outputs before a reset. Running the notebook does not publish data or mount Google Drive. The notebook can download the three approved public sources directly, so no real student upload is needed.

The public UCI licence permits attributed reuse, but the project's RAI2 publication rule is stricter: do not publish real row-level profiles. `.gitignore` guards the relevant CSV paths. Source identity, acquisition dates and licences are in `source_registry.json`. No source contains real UTM student records.
