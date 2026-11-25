# Explainable Student Dropout Prediction Using Early Academic Indicators

> An offline educational prototype for academic advisors and evaluators to compare early student outcome predictions, inspect explanations, and understand their limitations.

**Student:** Woo Yong Kang — A24AI0123  
**Course:** SAIA3113 — AI Engineering  
**Project stage:** Week 3 data preparation and executable V1 pipelines completed, with the saved Google Colab run from 12 November 2026 now included. Model development and evaluation remain planned.

## Problem Statement

Early student-support decisions require information available at the prediction point and understandable outputs. This project compares enrolment-only and first-semester machine learning models, with SHAP explanations and a cited reference guide. It uses a public benchmark and will not make decisions about real students.

## Evidence of the Problem

- Realinho et al. [1] describe dropout prediction supporting a tutoring team.
- Martins et al. [2] show why prediction timing deserves explicit evaluation.

These studies motivate the project; they do not establish a UTM-specific dropout problem.

## Initial Related Work / Existing Approaches

- **Realinho et al. (2022) [1]:** Public student-outcome dataset; transfer to another institution requires validation.
- **Martins et al. (2023) [2]:** Phased prediction; remaining limitations include class imbalance and course-specific differences.
- **Karimi-Haghighi et al. (2021) [3]:** Calibration and fairness at enrolment; does not evaluate this project's two-timepoint UCI comparison.

## Engineering Gap / Limitation

Build a reproducible comparison that documents feature timing, prevents leakage, reports class-sensitive errors, and connects predictions to explanations and cited limitations. The contribution is a bounded engineering implementation, not a claim that phased prediction is new.

## Project Objectives

- **O1:** Prepare and document enrolment-only and first-semester feature sets, excluding later or ambiguously timed information.
- **O2:** Develop Logistic Regression, Random Forest, and XGBoost pipelines, SHAP explanations, and a source-linked reference guide.
- **O3:** Compare macro-F1, dropout precision/recall, balanced accuracy, explanation changes, and relevant error patterns.

## Target Users

Academic advisors and student-support staff are the intended demonstration audience. The student developer and academic evaluators will inspect the research prototype. Real UTM student assessment is outside scope.

## Data Sources

- **Training data and public document 1:** UCI dataset and online documentation [4] — https://doi.org/10.24432/C5MC89
- **Public document 2:** Dataset descriptor [1] — https://doi.org/10.3390/data7110146
- **Public document 3:** Phased prediction study [2] — https://doi.org/10.3390/app13084702
- **Supporting research:** Calibration and fairness study [3] — https://arxiv.org/abs/2103.09068

The documents support feature definitions and the reference guide; the CSV supplies labelled training records. Public documents are not counted as separate training datasets.

## Evaluation and Responsible AI

Use the same stratified held-out split for both timepoints, with training-only preprocessing and tuning. Compare against a majority-class baseline and report class-sensitive metrics, confusion matrices, and SHAP explanations. Exclude second-semester variables. Examine subgroup errors where sample sizes allow.

Outputs will be labelled as research estimates. SHAP explanations are not causal conclusions. No automated admissions, scholarship, disciplinary, or support-allocation decisions are permitted within this scope.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `docs/week1_project_scope.md` | Individual Part C scope and full references |
| `docs/week1_observation_sheet.md` | Group Part A observation sheet |
| `docs/week1_system_map.png` | Group Part B system map |
| `data/` | Source records and future data documentation |
| `src/` | Reusable Week 3 data pipeline implementation |
| `notebooks/` | Executable Week 3 notebook and future experiments |
| `evaluation/` | Future metrics, error analysis, and evaluation evidence |
| `prompts/` | Reserved for later course work; no LLM prompts required at this stage |

See the [full Week 1 project scope](docs/week1_project_scope.md).

## Topic 2 Lab deliverables

| Part | Deliverable |
| --- | --- |
| A | [Project framing, scope and requirements](docs/week2_requirements.md) |
| B | [Evaluation criteria](docs/week2_evaluation_criteria.md) |
| C | [V1 architecture diagram](docs/week2_architecture_v1.png) |
| C | [Architecture decisions and traceability](docs/week2_architecture_decisions.md) |

Each written part includes its reflection. All acceptance thresholds are proposed targets, not measured results. The [editable Draw.io diagram](docs/week2_architecture_v1.drawio) and [public document attribution](data/README.md) are also available.

## Topic 3 Lab deliverables

[Open the complete notebook in Google Colab](https://colab.research.google.com/github/ykwooga-afk/ai-engineering-labs/blob/main/notebooks/week3_pipeline.ipynb)

The notebook includes the saved Google Colab execution from 12 November 2026. To reproduce it, open the notebook, run all cells and save your new run. Missing approved inputs are downloaded and checked against their hashes. No ZIP upload, Drive mount or model API key is required.

| Part | Deliverable |
|---|---|
| A | [Data inventory and requirement traceability](docs/week3_data_inventory.md) |
| A–C | [Notebook with saved Google Colab execution outputs](notebooks/week3_pipeline.ipynb) |
| B | [Preparation comparisons and decisions](docs/week3_preparation_decisions.md) |
| B | [Feature policy](docs/week3_feature_policy.csv) and [common lineage](data/week3_manifest.json) |
| C | [Pipeline PNG](docs/week3_pipeline_diagram.png) and [editable Draw.io source](docs/week3_pipeline_diagram.drawio) |
| C | [Pipeline decisions, stage contracts and traceability](docs/week3_pipeline_decisions.md) |
| C | [Reusable implementation](src/week3_pipeline.py) and [configuration](data/pipeline_configuration.json) |
| C | [Tabular run manifest](data/pipeline_v1/tabular/pipeline_manifest.json) and [document run manifest](data/pipeline_v1/documents/pipeline_manifest.json) |
| C | [Repeatability / Part B parity](evidence/week3_repeatability.json) and [fresh-workspace / failure checks](evidence/week3_independence_and_failures.json) |

**Observed results:** 4,424 prepared table rows; 8 T0 / 14 T1 predictors; 168 document chunks over 32 pages. Both branches pass repeated-run comparison and fresh-workspace execution; all 8 prepared output files match Part B. All 16 notebook code cells completed in the saved Google Colab run without error outputs, and the Part A/B checks recorded 37 passes. This is preparation and execution evidence, not a model-quality or fairness result.

**Execution provenance:** [Colab verification record](evidence/colab_execution_verification.json) identifies the exact saved notebook by SHA-256 and records Python 3.13.18, pandas 2.2.3 and pypdf 6.21.4. The notebook code and Markdown are unchanged from the earlier repository version. Existing standalone manifests, prepared files and earlier JSON execution records retain their original local-run provenance; they were not exported from the later Colab runtime. The Colab-specific evidence is the notebook's saved outputs and the verification record.

[Data access and private-output locations](data/WEEK3_STORAGE.md) explain the publication boundary inherited from RAI2. Row-level CSVs are not committed. The public notebook displays aggregate evidence; document excerpts retain CC BY attribution and page provenance. Full working data is included in the private Week 3 submission package or can be recreated by running the notebook.

## Weekly Progress

| Week | Focus | Deliverable | Status |
| --- | --- | --- | --- |
| W1 | Individual project framing | Project scope, README, public source links, and directory scaffold | Prepared |
| W1 | Group system analysis | Part A observation sheet and Part B system map | Existing group files retained in `docs/`; final group corrections remain to be checked |
| W2 | Parts A, B and C | Requirements, evaluation criteria, V1 architecture, decisions and traceability | Prepared; targets not yet evaluated |
| W3 | Parts A, B and C | Source inventory, prepared outputs, runnable batch pipelines, lineage, diagram and decisions | Local verification and saved Colab A–C execution available; model evaluation remains planned |

## References

[1] Realinho, V., et al. (2022). *Predicting Student Dropout and Academic Success*. Data, 7(11), 146. https://doi.org/10.3390/data7110146  
[2] Martins, M. V., et al. (2023). *Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education*. Applied Sciences, 13(8), 4702. https://doi.org/10.3390/app13084702  
[3] Karimi-Haghighi, M., et al. (2021). *Predicting Early Dropout: Calibration and Algorithmic Fairness Considerations*. https://arxiv.org/abs/2103.09068  
[4] Realinho, V., et al. (2021). *Predict Students' Dropout and Academic Success*. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89


