# Evaluation Criteria

**Project:** Explainable Student Dropout Prediction Using Early Academic Indicators\
**Course:** SAIA3113 AI Engineering | Topic 2 Lab Part B\
**Student:** Woo Yong Kang | A24AI0123\
**Version:** 1.0 | 5 November 2026\
**Status:** Evaluation plan only. No model results or user-study results are claimed.

This plan tests the requirements in [Part A](week2_requirements.md). All criteria begin with status **Not yet evaluated**. A failed target remains a failed target; absent or insufficient evidence is not a pass.

## Evaluation criteria table

| Criterion and objective / requirement IDs | Evaluation criterion | Capability bucket | Measurement method | Metric | Proposed threshold | User / business outcome |
| --- | --- | --- | --- | --- | --- | --- |
| E1 — O1 / FR1 / FR2 | Valid input and feature timing | Instruction-following capability | Audit all predictor columns and run 20 prohibited/invalid cases plus 20 valid fixture cases. Inspect split and preprocessing fit records. | Documented allowed columns; blocked invalid cases; accepted valid cases; leakage violations. | 100% included columns justified; 20/20 invalid cases blocked; 20/20 valid cases accepted; 0 timing or split-leakage violations. | Users do not receive apparently early predictions built from future or unsuitable information. |
| E2 — O3 / FR6 / FR7 / NFR1 | Class-balanced predictive performance | Domain-specific capability | Evaluate the training-selected model and majority baseline at both timepoints on the same held-out records. | Macro-F1 and gain over baseline; balanced accuracy as a secondary reported metric. | T0 macro-F1 >= 0.50; T1 >= 0.65; both >= baseline + 0.10. No independent acceptance threshold for balanced accuracy. | Evaluators can determine whether the model adds value beyond a trivial majority prediction. |
| E3 — O3 / FR7 / NFR2 | Dropout detection and false alarms | Domain-specific capability | Derive Dropout-vs-rest counts from locked three-class predictions; inspect confusion matrices. | Dropout precision and recall, with denominators and 95% intervals. | T0 recall >= 0.65, precision >= 0.60; T1 recall >= 0.75, precision >= 0.65. Both must pass at each timepoint. | Makes missed dropout cases and false labels visible together. |
| E4 — O2 / FR4 / FR5 / RAI4 | Explanation fidelity and source support | Domain-specific capability | Audit 20 explanation fixtures per timepoint and every substantive guide claim against its cited source passage. | Identity and displayed-contribution agreement; reconstruction residual; citation coverage and support. | 100% identity/display agreement; residual <= 0.0001 in declared output space; 100% claims cited and supported. | Users can inspect what the model used and verify the guide without mistaking an explanation for causation. |
| E5 — O3 / FR7 / RAI1 | Subgroup error disparities | Domain-specific capability | Compare gender and age partitions separately at each timepoint under the count rules below. | Maximum pairwise recall and FPR gaps; group counts and interval coverage. | Each estimable gap <= 0.10; all groups and planned intervals reported; insufficient groups marked inconclusive. | Exposes unequal error patterns and prevents unsupported fairness claims. |
| E6 — O1 / O2 / FR1 / FR3 / FR7 / RAI2 / RAI3 | Privacy, scope and visible limitations | Instruction-following capability | Run negative-input and prohibited-action suites; inspect runtime requests, 100 result screens and proposed publication files. | Prohibited-input rejection; disclosure completeness; prohibited actions, outbound record payloads and prohibited published profiles. | 100% prohibited inputs blocked; 100% required disclosures; 0 prohibited actions, external record payloads or prohibited published profiles. | Reduces the risk of identifying students, overtrust and unauthorised decisions. |
| E7 — O2 / FR3 / FR4 / NFR3 / NFR5 | Interactive latency and inference cost | Cost and latency | Time 50 sequential interactions per timepoint after warm-up; inspect model-call and billing records. | p90 end-to-end latency; external model calls; model API charges. | p90 < 3,000 ms at each timepoint; 0 calls; US$0 API charges. | Provides a responsive demonstration without requiring paid model access. |
| E8 — O2 / O3 / FR6 / FR7 / NFR4 | Repeatable evaluation | Domain-specific capability | Repeat the selected pipelines twice under the locked configuration. | Split/label agreement and maximum absolute metric difference. | 100% split/label agreement; difference <= 0.000001. | A reviewer can reproduce the reported comparison. |

The generation bucket is not applicable: V1 does not generate free-form answers. Instruction-following here means compliance with the application's declared input, output and scope rules; it does not imply use of an LLM.

## Common evaluation protocol

### Data and model selection

1. Record the public data version, download URL and SHA-256 checksum; assign internal row keys. Check duplicate records before splitting. Quarantine exact duplicate rows with the same label under a documented rule; quarantine conflicting duplicate records rather than silently choosing a label. Report any resulting change in sample size.
2. Make one stratified 80/20 train/test split with seed 42. Preserve the same row assignment for T0 and T1. Keep the test labels unavailable to feature, parameter and model selection.
3. On the training partition, use five-fold stratified cross-validation with seed 42. Fit encoders, scaling, imputation if needed, and any balancing procedure only on each training fold. Any explainer background sample also comes only from training data.
4. Compare the three Week 1 candidate families under the same folds and a recorded finite tuning budget. Select one model per timepoint by highest mean validation macro-F1. For scores within 0.005, prefer lower measured validation inference time; if still tied, prefer the simpler model. Record all candidates, not just the winner.
5. Fit the selected configuration on the full training partition. Freeze its feature lists, preprocessing, class order, decision rule and explanation settings before opening the test results. Use three-class argmax for labels, with a fixed documented class-order tie rule. Do not tune a Dropout threshold on the test set.
6. Evaluate once on the test partition and compare with a majority-class baseline fitted on training labels. Report both timepoints, class supports and confusion matrices. T1 minus T0 metric differences are informative even if T1 does not improve. Record failures without retuning on this test set.

This random split estimates within-benchmark generalisation. It is not a chronological future-cohort test or an evaluation on Malaysian students. Any later revision after seeing test results must acknowledge that the old test set is no longer a fresh confirmatory evaluation.

### Metric definitions and uncertainty

- **Macro-F1:** arithmetic mean of the F1 scores for Dropout, Enrolled and Graduate, with all three labels fixed in evaluation. A class with no predicted positives receives F1 zero and a warning.
- **Balanced accuracy:** mean recall across the same three classes.
- **Dropout precision:** TP / (TP + FP); **Dropout recall:** TP / (TP + FN). If there are no predicted Dropout cases, report precision as undefined and fail the precision target; do not count it as a pass.
- **Dropout false-positive rate:** FP / (FP + TN), treating Enrolled and Graduate as non-Dropout only for this error calculation. The trained task remains three-class classification.
- **Uncertainty:** use 1,000 fixed-seed, class-stratified bootstrap resamples of test predictions for 95% percentile intervals. Use paired resamples for T1-minus-T0 comparisons. For subgroup error intervals, resample within each subgroup and outcome stratum. Report skipped/undefined estimates rather than hiding them.
- **p90 latency:** the 45th ordered duration out of 50 interactions (nearest-rank definition), calculated separately for T0 and T1. Time the complete prepared path through the display boundary.

Acceptance uses the declared point-estimate thresholds; intervals communicate uncertainty and do not establish deployment readiness. Record raw durations, counts and metric calculations in later evidence.

### Fixed control workloads

**Input checks:** prepare 20 invalid cases: four missing or malformed-field cases; four invalid codes/ranges; four forbidden target or future-feature cases; four injected direct-identifier or unknown-field cases; and four unsupported timepoint or unapproved-record cases. Add 20 valid fixtures, ten per timepoint. These counts are planned workloads, not completed tests.

**Scope checks:** prepare ten prohibited-action cases: two each for admissions decisions, scholarship decisions, disciplinary decisions, support-allocation decisions and personalised intervention instructions. The interface must not expose these operations; any callable application route must also reject an unsupported operation, rather than relying only on a warning.

**Timing and disclosures:** select 50 approved fixtures per timepoint using a fixed, documented sampling rule. Include all predicted classes where available and disclose missing classes. Retain individual records only in the controlled evaluation environment; publish aggregate timing and clearly synthetic screenshots. The cold start and precomputation time are reported separately, without being hidden in the warm latency figure.

**Explanation checks:** preselect 20 fixtures per timepoint from the timing set, including varied classes and estimates where available. Compare model identity, selected class, timepoint, feature names, contribution signs and top-three ordering. Use the full contribution vector for reconstruction. The explanation cache must be keyed by model version, timepoint, input fingerprint, class and explanation configuration; stale entries fail the test. Global explanations use a fixed documented sample and the same field grouping and output scale for each comparison.

**Reference checks:** keep a claim ledger linking every substantive guide statement to its source URL, page/section and supporting passage. Check every claim rather than sampling. Explanations of prediction limitations must distinguish source facts from this project's design choices.

### Subgroup audit and failure handling

Audit the recorded gender categories and the project-selected age groups (<25 and >=25), separately for T0 and T1. These are feasible initial partitions, not a complete analysis of all protected or socioeconomic groups. Do not infer missing identity attributes.

Require at least 30 actual Dropout cases in a group for recall and 30 non-Dropout cases for FPR. Compare a metric only when at least two groups meet its denominator rule. Otherwise mark that comparison inconclusive. Report every group's count, including excluded or unknown categories, and the maximum pairwise absolute gap for each eligible metric.

E5 passes only when all planned comparisons are estimable and within the tolerance. Any excessive gap causes a fail; otherwise any unsupported comparison causes an inconclusive result. The report can be complete even when the fairness target fails. Investigate preprocessing, sample coverage and error patterns without claiming that a benchmark audit proves fairness in deployment.

### Evidence to retain later

The future `evaluation/` evidence should include the split manifest, run configuration and checksums, aggregate performance tables, confusion matrices, subgroup report, claim ledger, explanation checks, control-test results, timing log and reproducibility comparison. Evidence filenames are implementation choices; the evidence itself must identify the relevant E, FR, NFR and RAI IDs. Do not publish row-level sensitive profiles or pretend these planned files already exist.

## Part B reflection

E3 is the most important usefulness criterion because the intended demonstration concerns students who may need support. High overall performance can still hide missed dropout cases. Recall shows how many actual dropout cases are detected, while the precision floor stops the system from satisfying recall by labelling nearly everyone. I would interpret E3 only after the feature-timing check passes, and alongside subgroup errors and the prototype's limits. Passing it would support a benchmark demonstration, not prove that a real intervention improves retention.
