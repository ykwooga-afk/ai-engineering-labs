# Week 1 Project Scope

**Course:** SAIA3113 — AI Engineering  
**Student:** Woo Yong Kang  
**Matric number:** A24AI0123  
**Date:** 29 October 2026  
**Activity:** Topic 1 Lab, Part C — Individual Semester Project

## 1. Project Name

**Explainable Student Dropout Prediction Using Early Academic Indicators**

Short name: **Explainable Student Dropout Prediction**  
Suggested repository name: `ai-engineering-student-dropout`

## 2. Domain

Higher education, educational data mining, and explainable machine learning.

## 3. Problem Statement

Academic advisors need to understand which students may require additional support, but early predictions must rely on information available at the time they are made. A model evaluated using later academic results may look useful while being unsuitable for an earlier decision point. A prediction also needs an explanation and a clear statement of its limitations before a person can interpret it responsibly.

This project will build an offline research prototype comparing student outcome predictions at enrolment and at the end of the first semester. It will compare Logistic Regression, Random Forest, and XGBoost, and use SHAP to explain model outputs. The prototype will include a small, cited reference guide based on public documents to explain the dataset, prediction timing, and interpretation limits.

Machine learning is appropriate because the task involves learning and comparing relationships among several academic indicators. Its value will be tested against a majority-class baseline; an improvement will not be assumed. The prototype will not make admissions, scholarship, disciplinary, or student-support decisions.

## 4. Evidence of the Problem

**Evidence 1 — A documented need for early support.** Realinho et al. (2022) describe dropout prediction as part of a learning analytics tool supporting a tutoring team. This provides a concrete educational use case for examining student outcomes. It does not establish a dropout rate or a deployment need at UTM. [1]

**Evidence 2 — Timing affects the usefulness of predictions.** Martins et al. (2023) compare prediction phases and report their best results at the end of the first semester. This motivates explicitly comparing earlier availability with predictive performance instead of evaluating all features together. [2]

## 5. Initial Related Work / Existing Approaches

| Study / solution | Relevant contribution | Key limitation for this project |
| --- | --- | --- |
| Realinho et al. (2022), *Predicting Student Dropout and Academic Success* [1] | Provides a public dataset and describes its educational context. | Data from one Portuguese institution does not establish performance for Malaysian students. |
| Martins et al. (2023), *Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education* [2] | Compares phased prediction models. | The authors report remaining class imbalance effects and do not account for course- and school-specific differences. |
| Karimi-Haghighi et al. (2021), *Predicting Early Dropout: Calibration and Algorithmic Fairness Considerations* [3] | Examines calibrated enrolment-time predictions and group error disparities. | Its enrolment-time evaluation does not answer this project's comparison with first-semester information on the UCI dataset. This is a scope difference, not a criticism of the study. |

## 6. Engineering Gap / Limitation

The practical task is to produce a reproducible workflow that keeps feature availability, model comparison, explanations, and limitations consistent. A single accuracy score does not show whether future information entered the pipeline, whether dropout cases are missed, or how explanations change when first-semester information becomes available.

This semester project will address that task through two documented feature sets, a common evaluation split, class-sensitive metrics, SHAP explanations, and a source-linked interpretation guide. Phased prediction already exists in the literature [2]; this project is a bounded engineering implementation and comparative study, not a claim that the approach is novel.

## 7. Initial Project Objectives

**O1 — Design:** To prepare and document enrolment-only and first-semester feature sets, with a feature-availability table and citations to the public data documentation, excluding later or ambiguously timed information.

**O2 — Develop:** To implement reproducible Logistic Regression, Random Forest, and XGBoost pipelines, with SHAP explanations and a document-grounded reference guide describing the data and output limitations.

**O3 — Evaluate:** To compare both prediction points using macro-F1, dropout precision and recall, and balanced accuracy; examine changes in SHAP explanations; and report error patterns and relevant Responsible AI limitations.

## 8. Target Users

- **Primary intended users:** Academic advisors and student-support staff reviewing an educational demonstration of predictive outputs and their limitations.
- **Evaluation users:** The student developer and academic evaluators inspecting reproducibility, feature timing, and model performance.
- **Potential beneficiaries:** Students who could benefit from better-informed support in a future, separately validated application.

The semester prototype will use public benchmark data. It will not assess real UTM students or claim institutional readiness.

## 9. Data Sources and Public Documents

The project has one tabular training dataset and three public documents for its reference guide. These serve different purposes: documents explain the data and interpretation constraints; they are not additional labelled training datasets.

| Source | URL | Planned use |
| --- | --- | --- |
| UCI *Predict Students' Dropout and Academic Success*: dataset and online documentation [4] | https://doi.org/10.24432/C5MC89 | CSV for model training/evaluation; documentation for feature definitions, outcome labels, and provenance. This is public document 1. |
| Realinho et al. (2022), dataset descriptor [1] | https://doi.org/10.3390/data7110146 | Public document 2: dataset context and limits, used in the cited reference guide. |
| Martins et al. (2023), phased prediction study [2] | https://doi.org/10.3390/app13084702 | Public document 3: prediction timing and evaluation context, used in the cited reference guide. |
| Karimi-Haghighi et al. (2021) [3] | https://arxiv.org/abs/2103.09068 | Supporting research for calibration and fairness considerations. |

The UCI release contains 4,424 records, 36 input features, and the target classes **Dropout**, **Enrolled**, and **Graduate**. The outcome is recorded at the end of the normal course duration; it is not a label for dropping out during the first semester. UCI lists the data under CC BY 4.0. [4]

The reference guide will contain short, manually checked explanations with source links. It will help users understand what the outputs mean and what they cannot establish. A generative chatbot or a retrieval-augmented generation service is not required for the initial scope.

Only source links, original documentation, and permitted artefacts will be committed. The signed FYP proposal, personal contact information, and confidential student records will not be included. Source access date: 29 October 2026.

## 10. Similar to EduAdvisor

Both projects address higher education, define specific users, use publicly accessible documents, and need transparent outputs, objective evaluation, and human oversight. Both will keep requirements, data documentation, evaluation evidence, and limitations in GitHub.

## 11. Different from EduAdvisor

EduAdvisor answers academic questions using university documents. This project predicts predefined student outcome categories from tabular records and explains those predictions. Public documents support the reference guide and data definitions. Its main evaluation measures are classification performance and error patterns, rather than conversational answer quality. It does not provide university policy advice or personalised intervention instructions.

## 12. Responsible AI Risks and Controls

| Risk | Who may be harmed and how | Planned control / evaluation |
| --- | --- | --- |
| False positives and stigma | A student could be unfairly labelled as likely to drop out. | Restrict the project to an offline demonstration; report dropout precision and false positives; prohibit automated institutional decisions. |
| False negatives | Students who need support could be overlooked. | Report dropout recall and the confusion matrix; explain that a low model score cannot establish that support is unnecessary. |
| Unequal error rates | Demographic or socioeconomic groups could receive unequal treatment. | Where sample sizes permit, examine subgroup recall and false-positive rates with group counts. Small groups will be marked inconclusive. Removing sensitive features alone will not be treated as proof of fairness. |
| Privacy and re-identification | Combining public records with outside information could expose individuals. | Use the public benchmark only; avoid linkage, identifying fields, and personal records; publish aggregate findings rather than identifiable profiles. |
| Overtrust and misleading explanations | Advisors may interpret a prediction or SHAP value as certainty or a cause of dropout. | Label outputs as model estimates; explain that SHAP reflects model associations, not causal effects; include cited interpretation limits. |
| Poor transfer to another institution | Users could apply results to UTM students without validation. | Clearly state the source population and exclude real institutional deployment from scope. |

## 13. Initial Engineering and Evaluation Plan

### Feature availability

The enrolment model will use only variables supported as available at enrolment. The first-semester model will add eligible first-semester academic indicators. Both will exclude all second-semester indicators and the target from their inputs. Variables such as debtor status, tuition-fee status, or scholarship status will be excluded unless their measurement time can be justified. The feature list will be finalised after a column-level audit.

### Reproducible evaluation

Use the same stratified 80/20 training/test split and fixed random seed for both prediction points. Keep the held-out test set untouched during model selection. Fit encoders, scaling, and any class-balancing procedure within training folds only. Use training-only stratified cross-validation for tuning and compare against a majority-class baseline.

Report macro-F1, balanced accuracy, dropout precision/recall, and confusion matrices. Compare the two timepoints on the same held-out records. Document uncertainty and model limitations. A random held-out split measures within-dataset generalisation; it does not demonstrate performance on future cohorts or other universities. No performance results are claimed in Week 1.

### Explanations and reference guide

Produce global SHAP summaries and a small selection of local explanations for anonymised or synthetic demonstration cases. Record the model, class, and background sample used. Check whether the explanation shown corresponds to the selected model output. Validate reference-guide statements against the three public documents and ensure each substantive statement has a source link.

### Feasibility and deliverables

The project will use Python, pandas, scikit-learn, XGBoost, SHAP, Jupyter/Colab, and Git. The small tabular dataset and three model families make the initial scope manageable within one semester. Planned outputs are reproducible notebooks, a feature-availability table, model comparisons, SHAP visualisations, the reference guide, and a limitations report. No paid API or dedicated GPU is required for the planned scope.

Week 1 covers scoping and the repository record. Implementation and measured results will be added in subsequent weeks.

## References

1. Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). Predicting Student Dropout and Academic Success. *Data, 7*(11), 146. https://doi.org/10.3390/data7110146
2. Martins, M. V., Baptista, L., Machado, J., & Realinho, V. (2023). Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education. *Applied Sciences, 13*(8), 4702. https://doi.org/10.3390/app13084702
3. Karimi-Haghighi, M., Castillo, C., Hernández-Leo, D., & Moreno Oliver, V. (2021). Predicting Early Dropout: Calibration and Algorithmic Fairness Considerations. *Companion Proceedings of the 11th International Conference on Learning Analytics & Knowledge (LAK21)*. Preprint: https://arxiv.org/abs/2103.09068
4. Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). *Predict Students' Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89
