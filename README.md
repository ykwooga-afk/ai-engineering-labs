# Explainable Student Dropout Prediction Using Early Academic Indicators

> An offline educational prototype for academic advisors and evaluators to compare early student outcome predictions, inspect explanations, and understand their limitations.

**Student:** Woo Yong Kang — A24AI0123  
**Course:** SAIA3113 — AI Engineering  
**Project stage:** Week 1 scoping; implementation and evaluation are planned.

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
| `src/` | Future reusable implementation |
| `notebooks/` | Future experiments |
| `evaluation/` | Future metrics, error analysis, and evaluation evidence |
| `prompts/` | Reserved for later course work; no LLM prompts required at this stage |

See the [full Week 1 project scope](docs/week1_project_scope.md).

## Weekly Progress

| Week | Focus | Deliverable | Status |
| --- | --- | --- | --- |
| W1 | Individual project framing | Project scope, README, public source links, and directory scaffold | Prepared |
| W1 | Group system analysis | Part A observation sheet and Part B system map | Existing group files retained in `docs/`; final group corrections remain to be checked |
| W2 | Requirements refinement | Confirm feature availability and evaluation criteria | Planned |

## References

[1] Realinho, V., et al. (2022). *Predicting Student Dropout and Academic Success*. Data, 7(11), 146. https://doi.org/10.3390/data7110146  
[2] Martins, M. V., et al. (2023). *Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education*. Applied Sciences, 13(8), 4702. https://doi.org/10.3390/app13084702  
[3] Karimi-Haghighi, M., et al. (2021). *Predicting Early Dropout: Calibration and Algorithmic Fairness Considerations*. https://arxiv.org/abs/2103.09068  
[4] Realinho, V., et al. (2021). *Predict Students' Dropout and Academic Success*. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89
