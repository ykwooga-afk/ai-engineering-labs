# Requirements Specification

**Project:** Explainable Student Dropout Prediction Using Early Academic Indicators\
**Course:** SAIA3113 AI Engineering | Topic 2 Lab Part A\
**Student:** Woo Yong Kang | A24AI0123\
**Version:** 1.0 | 5 November 2026\
**Status:** Planning specification. All thresholds below are proposed acceptance targets, not measured results.

This specification develops the [Week 1 project scope](week1_project_scope.md) into testable requirements for an offline educational prototype. It compares predictions made with enrolment information and with information available by the end of the first semester. The prototype supports inspection of benchmark results; it does not assess real UTM students or make institutional decisions.

## Section 0 Project framing and application scope

### Problem and evidence

Academic advisors need to understand both a prediction and the information available when it was made. Using later results in an early prediction would make its apparent usefulness misleading. Unexplained predictions also make errors difficult to question.

- **Evidence 1:** Realinho et al. describe a public student-outcome dataset used in a learning analytics tool that informs a tutoring team [1]. This supports the relevance of an advisor-facing demonstration, but does not establish a dropout problem at UTM.
- **Evidence 2:** Martins et al. compare prediction phases and report their best results at the end of the first semester [2]. This motivates testing the trade-off between earlier availability and predictive performance in our own controlled comparison.

### Existing approaches

| Study or approach | What it already addresses | Relevance and remaining project task |
| --- | --- | --- |
| Realinho et al. (2022) [1] | Publishes a student-outcome benchmark and describes its institutional context. | Provides data provenance. Our prototype still needs an explicit feature-timing policy and reproducible evaluation. |
| Martins et al. (2023) [2] | Evaluates phased prediction during the first academic year. | Establishes that phased prediction already exists. Our task is a bounded implementation with linked requirements, explanations and acceptance criteria. |
| Karimi-Haghighi et al. (2021) [3] | Studies enrolment-time prediction, calibration and group error disparities. | Motivates subgroup auditing and caution about probability interpretation. Its study does not replace evaluation on this project's dataset and feature sets. |

### Engineering gap

The practical gap is the need for one auditable workflow connecting feature availability, a fair model comparison, understandable explanations and explicit limits. A single accuracy score cannot establish that future information was excluded or that dropout cases and demographic groups are handled adequately. This is an engineering implementation and comparative study, not a claim of scientific novelty.

### Project objectives

- **O1 Design:** To define and document enrolment-only and first-semester feature sets, supported by source documentation, excluding later and ambiguously timed information.
- **O2 Develop:** To develop reproducible prediction pipelines, model explanations and a cited reference guide for an offline demonstration. Logistic Regression, Random Forest and XGBoost remain the candidate families from Week 1; SHAP remains the planned explanation method. These are candidate implementation choices, not substitutes for behavioural requirements.
- **O3 Evaluate:** To compare both prediction points using macro-F1, balanced accuracy, dropout precision and recall, explanation checks and subgroup error analysis, and report whether the proposed acceptance targets are met.

### Application scope

| Scope element | Definition |
| --- | --- |
| Intended users | Academic advisors and student-support staff viewing the demonstration; the developer and academic evaluators inspecting evidence. |
| Supported tasks | Select an approved demonstration record and prediction point; inspect class estimates and explanations; consult the cited guide; compare aggregate evaluation results. |
| Information domain | Student-outcome prediction, feature availability, benchmark definitions and interpretation limits. No university-policy advice. |
| Data source | UCI Predict Students' Dropout and Academic Success, with 4,424 records and 36 input features [4]. Predict the original three labels: Dropout, Enrolled and Graduate. |
| Target meaning | The recorded outcome at the end of the normal course duration [4]. Predicting at the end of semester one does not mean predicting dropout during semester one. Enrolled is retained as a distinct class. |
| Operating context | A single-user research notebook or lightweight local interface on CPU. Development may use Colab with public benchmark data. The demonstration uses prepared artefacts without external model APIs. |
| Important constraints | One-student semester workload; public data only; no paid inference service; no dedicated GPU requirement; uncertain feature timestamps; class imbalance; one source institution. |
| Explicit exclusions | Real UTM records, record linkage, live student monitoring, automated admissions, scholarship, disciplinary or support-allocation decisions, personalised intervention instructions, causal claims, and a general chatbot. |
| Evaluation focus | Whether each timepoint beats a trivial baseline under a leakage-controlled protocol, whether errors and limitations are visible, and whether the interface and explanations meet the declared controls. |

### Feature availability and assumptions

The following policy is fixed before training. The implementation will record each retained column, its source, allowed timepoint and exclusion reason where applicable.

| Feature group | Enrolment model T0 | First-semester model T1 | Rule |
| --- | --- | --- | --- |
| Documented admission and pre-entry information | Eligible | Eligible | Examples include admission grade, previous qualification and course. Retain only fields whose timing can be justified. |
| First-semester academic indicators | Excluded | Eligible | Use only values documented as available by the end of semester one. |
| Second-semester academic indicators | Excluded | Excluded | Later information must never enter either model. |
| Debtor, tuition-fee and scholarship status; any other uncertain snapshot | Excluded by default | Excluded by default | Add only after a documented timing justification and versioned specification change before model selection. |
| Gender and nationality | Audit only | Audit only | Kept separate from predictors in V1; omission does not establish fairness. Age may be an eligible enrolment predictor and also an audit variable. |
| Target and technical row identifiers | Excluded | Excluded | Target is used only for supervised learning and evaluation. Internal row keys support splits and are not predictors or public identifiers. |

T0 and T1 use the same held-out records. This is a retrospective feature-window comparison, not a validated prospective system for students still active at semester one. The available benchmark does not establish precise dropout dates or reliable deployment-time snapshots for every field. Neither UTM transferability nor the effect of an intervention will be claimed.

## Section 1 Functional requirements

| ID | Requirement — The system SHALL | Scope boundary — SHALL NOT |
| --- | --- | --- |
| FR1 | Allow selection of an approved public-benchmark demonstration fixture or synthetic case and either T0 or T1; validate required fields, codes and ranges before prediction and explain invalid input. | Accept arbitrary real-student uploads, identifiers or an unsupported prediction point. |
| FR2 | Apply the documented feature allowlist for the selected timepoint and use the matching fitted preprocessing and prediction artefacts. | Use the target, row identifiers, second-semester fields or unverified feature timing as predictors; fit preprocessing on held-out records. |
| FR3 | Return the predicted class and three class estimates, together with the timepoint and model version. | Treat an estimate as certainty, a calibrated personal risk, or an institutional decision. |
| FR4 | Show the three largest absolute feature contributions for a selected class, their direction, the explanation baseline and model identity; provide an aggregate feature-contribution view for each timepoint. | Describe feature contributions as causes or show an explanation from a different model, class or timepoint. |
| FR5 | Provide a manually checked reference guide on the data, prediction timing and interpretation limits, with a source link and section locator for each substantive claim. | Invent source support, answer unrelated questions or provide personalised intervention advice. |
| FR6 | Compare the candidate model families and a majority-class baseline at both timepoints using the same split and training-only selection protocol. | Select features, tune settings or choose the final model from held-out test results. |
| FR7 | Produce an aggregate report containing required metrics, confusion matrices, subgroup counts and errors, explanation checks, limitations and pass/fail/inconclusive outcomes against this specification. | Publish identifiable profiles, hide a failed criterion or describe missing evidence as a pass. |

## Section 2 Non-functional requirements

| ID | Quality attribute | Requirement | Measurement method | Metric | Proposed threshold |
| --- | --- | --- | --- | --- | --- |
| NFR1 | Predictive quality | The selected model at each timepoint shall improve class-balanced performance over the majority-class baseline. | Apply the locked evaluation protocol in Part B to the held-out test set. | Three-class macro-F1; absolute macro-F1 gain over baseline. | T0 macro-F1 >= 0.50; T1 >= 0.65; each >= its baseline + 0.10. |
| NFR2 | Error balance | The selected model shall identify dropout cases without ignoring false alarms. | Compute Dropout-vs-rest precision and recall from the same test predictions. | Dropout recall and precision. | T0 recall >= 0.65 and precision >= 0.60; T1 recall >= 0.75 and precision >= 0.65. |
| NFR3 | Response time | The prepared demonstration shall display a complete result within the interactive latency target. | Time 50 sequential valid interactions per timepoint on the documented CPU environment, after one disclosed warm-up. Include validation, prediction, explanation retrieval and display preparation. | p90 end-to-end latency per timepoint. | < 3,000 ms for each timepoint. Training, installation and precomputation are measured separately. |
| NFR4 | Reproducibility | A repeated evaluation in the same documented environment shall reproduce the recorded split, predictions and headline metrics. | Repeat the selected pipelines twice with fixed seeds, data checksum and pinned dependencies. | Split and predicted-label agreement; maximum absolute difference in required metrics. | 100% split/label agreement; metric difference <= 0.000001. |
| NFR5 | Inference cost | The demonstration shall require no paid model API or external model call for prediction and explanation display. | Inspect runtime dependencies and outgoing requests during the 100 timed interactions; review any usage ledger. | External model calls; billable model API cost. | 0 external model calls and US$0 model API charges. Compute, electricity and internet are not claimed to be free. |

These are project-selected targets, not published standards or achieved scores. The higher T1 targets reflect its additional academic information; they do not presume improvement. A 0.10 macro-F1 margin requires a meaningful improvement over a trivial baseline. The precision floors prevent pursuing recall by simply flagging most records. Three seconds is a proposed tolerance for this small demonstration. Any target revision must be justified and versioned before inspecting held-out results; a missed target is reported honestly.

## Section 3 Responsible AI requirements

| ID | Risk | Requirement | Measurement method | Metric | Proposed threshold |
| --- | --- | --- | --- | --- | --- |
| RAI1 | Unequal errors | The system shall report subgroup dropout recall and false-positive rate with counts and uncertainty, and flag excessive gaps or insufficient evidence. | Evaluate the selected model separately at T0 and T1 by recorded gender and age at enrolment (<25 / >=25). Compare eligible groups within each partition. | Maximum pairwise absolute recall gap and FPR gap; audit coverage. | Each estimable gap <= 0.10 (10 percentage points); 100% planned groups reported. An under-supported comparison is inconclusive, never a fairness pass. |
| RAI2 | Privacy and re-identification | The system shall restrict input to approved fixtures, reject identifying or unknown fields, avoid record linkage, and publish only aggregates and clearly synthetic local examples. | Run the 20-case negative suite in Part B; inspect the request trace and all candidate publication files. | Rejected prohibited inputs; external record payloads; identifying fields or real row-level profiles in published outputs. | 100% prohibited inputs rejected; 0 external record payloads; 0 prohibited published profiles or identifiers. |
| RAI3 | Overtrust and misuse | Every result shall identify its model and timepoint and state that it is a research estimate, that explanations are associative, and that the prototype is not validated for UTM decisions. | Audit all 100 timed result screens and exercise 10 prohibited-action cases. | Required-disclosure completeness; prohibited actions completed. | 100% screens contain all disclosures; 0 automated institutional decisions or personalised intervention outputs. |
| RAI4 | Misleading evidence and explanations | The system shall show only source-supported guide claims and explanations corresponding to the actual model output. | Audit every substantive guide claim and 20 explanation fixtures per timepoint; compare displayed contributions with saved explainer values. | Citation coverage and support; model/class/timepoint and top-three contribution agreement; additivity residual. | 100% claims cited and supported; 100% explanation identity and display agreement; residual <= 0.0001 in the declared model-output space for all 40 fixtures. |

For RAI1, a group needs at least 30 actual Dropout records for recall and 30 non-Dropout records for FPR. A comparison needs at least two eligible groups; otherwise mark that comparison inconclusive. Report both denominators even when a metric is unavailable. These are screening rules, not a guarantee of statistical adequacy or fairness. Report 95% bootstrap intervals and do not interpret the point-estimate tolerance as evidence of deployment readiness. If a gap exceeds the tolerance, the criterion fails even when the system correctly flags it.

For RAI4, record the explanation's class, background data, output scale and full contribution vector. Check baseline plus the full vector against the corresponding model output; the displayed top three alone need not sum to that output. Aggregate one-hot contributions to original fields before ranking and show the contribution of the remaining fields as a remainder. If the method cannot support a valid reconstruction check, record a failure or a justified, versioned change before testing.

### Part A reflection

RAI1 will be the most difficult requirement to measure convincingly. Some groups may contain too few dropout cases for stable recall estimates, and a small observed gap can hide uncertainty. The dataset also represents a different institutional setting from UTM. I will report denominators and intervals, mark unsupported comparisons inconclusive, and avoid claiming that removing demographic predictors makes the model fair. This makes the limitation visible even when the prototype cannot resolve it.

## References

Sources checked on 5 November 2026. The thresholds and design decisions above are proposed for this project; they are not attributed to these papers.

1. Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). *Predicting Student Dropout and Academic Success*. Data, 7(11), 146. https://doi.org/10.3390/data7110146
2. Martins, M. V., Baptista, L., Machado, J., & Realinho, V. (2023). *Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education*. Applied Sciences, 13(8), 4702. https://doi.org/10.3390/app13084702
3. Karimi-Haghighi, M., Castillo, C., Hernández-Leo, D., & Moreno Oliver, V. (2021). *Predicting Early Dropout: Calibration and Algorithmic Fairness Considerations*. LAK21 companion proceedings; author preprint. https://arxiv.org/abs/2103.09068
4. Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). *Predict Students' Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89. CC BY 4.0.
