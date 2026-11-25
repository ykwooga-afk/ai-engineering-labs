# Data Quality, Bias, and Responsible Data Report — Explainable Student Dropout Prediction Using Early Academic Indicators

**Name:** Project author  
**Course:** SAIA3113 AI Engineering — Topic 4 Lab  
**Review date:** 25 November 2026

This report continues the same project from Topics 1–3. The main task is an offline, three-class comparison of enrolment (T0) and end-of-first-semester (T1) predictors. The papers support a manually checked reference guide. They are not training labels, and this project has not implemented a chatbot or RAG system.

The input is pinned to Lab 3 commit `808330bf96c995353e46038f960e25e455474842`. Our actual Lab 3 text file was `data/processed/prepared_text.jsonl`. The notebook explicitly creates the course hand-off names `prepared_chunks.jsonl` and `chunks.pkl`, then verifies all 168 texts and metadata dictionaries match the original. This is a format adapter, not a claim that those names were already present. The UCI table is separately checked against its Lab 3 SHA-256. No model training, embeddings, retrieval or model API calls are performed.

## 1. Data Quality Scorecard

The ratings are engineering judgements within this project's scope: 1 = critical uncontrolled gap; 2 = substantial unresolved gap; 3 = material gap contained by restrictions; 4 = scoped checks pass with documented limits; 5 = complete evidence for the declared scope. N.V. means the dimension cannot be established from the checks performed. Ratings are not percentages or model scores.

| Dimension | Rating (1–5 / N.V.) | Evidence | Action / limitation |
|---|---:|---|---|
| Completeness | 3 | 168/168 chunks contain text and source metadata; the table has 4,424 rows and no null cells. However, 78 paper chunks are held, reducing available feature-definition evidence. | Use original source pages for definitions. Do not equate populated fields with complete meaning or coverage. |
| Consistency | 4 | Source hash, URL, version, licence, page range and character-span checks pass. JSONL and PKL contents agree. T0 has 8 predictors and T1 has 14, with the same exclusions as Topic 3. | Keep the UCI 4,424-row release distinct from the 4,433-record study described in S03, page 4. The cause of that difference remains N.V. |
| Accuracy | N.V. | Source-page inspection confirms repeated and displaced text in S02 extraction. S03 page 8 has a legitimate sentence continuing onto page 9. Only a sample and targeted cases were examined. | Quarantine affected S02 pages. Verify every substantive future guide claim against the PDF; no full-corpus factual-accuracy claim. |
| Timeliness | N.V. | Source versions and access dates are recorded. S02 was published in 2022 and S03 in 2023; S03 describes a historical institutional cohort. No current Malaysian cohort is supplied. | These versions are usable for a fixed benchmark exercise. Current cohort relevance and deployment-time snapshot validity are not established. |
| Uniqueness | 4 | Normalised-text hashing finds 9 duplicate extras in 4 groups; all occur inside the 78 quarantined records. The 90 retained texts have 90 distinct hashes. No exact duplicate table rows or predictor profiles were found. | Exact hashing does not find paraphrases, near-duplicates, conflicting versions or distinct people with similar profiles. |

The quality gate was planned around these two Topic 2 requirements before choosing rules:

| Requirement | Required data / dimensions | Observable check | Decision |
|---|---|---|---|
| FR2: use only justified features at T0 and T1 | Consistency, accuracy and timeliness of feature definitions and availability | Match 8/14-column allowlists; exclude Target, row keys, semester-two fields, audit-only and uncertain snapshot fields | Stop on forbidden fields; retain uncertain fields outside predictors |
| FR5: provide a traceable, manually checked reference guide | Completeness, accuracy, consistency and uniqueness of source evidence | Check source identity and locators; inspect pages, short fragments and duplicates | Quarantine unreliable extraction; retain other text only for source-checked manual use |

## 2. Validation and Data-Defect Findings

Twelve rules were actually run with Pandera using lazy validation. The table below uses the **168 input chunks** as its denominator. There are **249 rule flags on 127 distinct chunks**; the flags overlap and must not be added as separate defective records. The detailed evidence is in `week4_validation_failures.csv`, and the original Pandera output is in `week4_pandera_failure_cases.csv`.

| rule | field | condition | failures | percent | action | reason |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | missing_text | Nonblank text | 0 | 0.0 | Hard fail | Empty evidence cannot support FR5. |
| R2 | missing_source | Nonblank source | 0 | 0.0 | Hard fail | A passage must be traceable. |
| R3 | corrupted_char | No NUL or U+FFFD | 0 | 0.0 | Quarantine | These characters indicate damaged extraction, not all possible corruption. |
| R4 | provenance_ok | Hash, URL, version and licence equal source registry | 0 | 0.0 | Hard fail | Prevents source/version drift. |
| R5 | page_ok | Page in source-specific range: S02 1–17; S03 1–15 | 0 | 0.0 | Hard fail | Supports page-level verification. |
| R6 | span_ok | Original end minus start equals original text length | 0 | 0.0 | Hard fail | Protects inherited source offsets. |
| R7 | short_chunk | At least 100 characters | 2 | 1.19 | Review | A screening threshold for boundary fragments; not proof that short text is wrong. |
| R8 | extraction_risk | No inherited peer-review extraction warning | 78 | 46.43 | Quarantine pending re-extraction | Known affected pages have unreliable reading order; apply a conservative page-level hold. |
| R9 | table_order_risk | No inherited table reading-order warning | 104 | 61.9 | Review | Linear text can lose table relationships even when valid Unicode. |
| R10 | publisher_sidebar | No inherited publisher sidebar warning | 10 | 5.95 | Review | Front matter can displace task-relevant evidence. |
| R11 | noisy_whitespace | No run of four spaces or four newlines | 0 | 0.0 | Review | Detects gross whitespace noise only. |
| R12 | dense_page | No inherited dense-extraction warning | 55 | 32.74 | Review | Unusual page volume is a warning, not an independent deletion rule. |

The 100-character threshold is a warning to inspect fragments. It is not a requirement that all meaningful passages exceed 100 characters. Page ranges come from the two actual PDFs. The source-specific warning rules reuse metadata captured in Topic 3 rather than inventing new source classifications.

| Issue category | Observed evidence | Interpretation and action |
|---|---|---|
| Missing | 0 blank texts, 0 missing source paths; 0 table null cells | Structural completeness passes. Separately, 142 rows have an explicit unknown code in at least one parent's qualification; no-null does not mean all information is known. These fields are already excluded from predictors. |
| Corrupted | 0 NUL or replacement-character cases | This narrow character test passes. It does not catch damaged table relationships or repeated text. |
| Noisy | 0 gross-whitespace flags; 10 publisher-sidebar flags; 55 dense-extraction flags | Formatting checks alone miss irrelevant front matter and duplicated content. Keep flags visible. |
| Inconsistent | 0 provenance, page-range or span failures; 104 table-order warnings | Metadata consistency passes. Reading order remains a review concern, not a proven error in every flagged chunk. |
| Duplicated | 9 extra occurrences in 4 exact-text groups | Preserve each occurrence's provenance. All groups are covered by extraction quarantine. |
| Stale | No record is labelled stale solely because it is old | The sources are fixed historical evidence. Present-day applicability is N.V.; age alone cannot decide fitness for a retrospective benchmark. |
| Uncertain | 78 inherited extraction-risk flags, incomplete semantic review, uncertain snapshot fields | Hold affected text pages; preserve the existing feature exclusions and source-check requirement. |

The deterministic sample used `random_state=42`: chunks 137, 30, 119, 29, 142, 161, 164, 51, 105 and 60. The notebook prints their full text and source locators. Bibliography chunks are legitimate source material but are not, by themselves, evidence for a substantive project claim. This is another limitation a simple length check would miss.

Three targeted triage decisions are recorded below; chunk numbers refer to the original zero-based input order, not newly renumbered records.

| Item / rule | Evidence checked | Interpretation | Decision and reason |
|---|---|---|---|
| Chunk 29, S02 page 5; R8/R9/R12 | The rendered page contains Tables 2–4. The extracted chunk includes a preceding analysis paragraph and its text occurs six times across chunks 21, 24, 27, 29, 32 and 35. | Actual extraction defect: repetition and displaced page content. | Quarantine the affected page's chunks rather than select an arbitrary copy as authoritative. |
| Chunk 51, S02 page 6; R8/R9/R12 | The original page contains Tables 5–8 in order. The chunk mixes first-semester values with tuition-fee and macroeconomic material from the previous page. | Actual extraction defect: row relationships and page order are unreliable. | Quarantine; consult the rendered PDF directly until a separate re-extraction is verified. |
| Chunk 142, S03 page 8; R7/R9 | The 91-character fragment matches the final line of page 8. Its sentence continues at the top of page 9. | Valid short exception, but not a self-contained statement. | Retain unchanged with `boundary_context_required=true`; require adjacent-page checking before use. |

**Manual-inspection reflection:** Valid words and numbers can appear in the wrong table row or page. A Unicode or length rule will pass this text because the symbols themselves are readable. Comparing the extracted passage with the visible table reveals the loss of meaning. Conversely, a short fragment can be valid when a sentence crosses a page boundary. These findings concern accuracy, consistency and completeness of context.

## 3. Duplicate and Anomaly Findings

Whitespace is normalised only for hashing: leading/trailing whitespace is removed and internal whitespace runs become one space. Stored source text is not rewritten. The duplicate groups have sizes 6, 3, 2 and 2, giving 9 extra occurrences. All source metadata dictionaries are retained in `all_provenance`, including source ID, SHA-256, URL, page and original offsets. `week4_duplicate_review.csv` identifies every extra occurrence and its decision.

The conservative hold covers all chunks on S02 pages 4, 5, 6, 7, 8, 9 and 11 because Topic 3 recorded extraction contamination for those pages. The targeted visual inspection confirms problems on pages 5 and 6; it does **not** prove that every passage on the other flagged pages is wrong. Holding the full affected page set prevents unverified passages from passing simply because a specific duplicate was removed. It may temporarily exclude valid material; that loss is visible in the coverage plot.

**Accounting:** 168 original chunks = 90 retained + 78 quarantined. The 9 duplicate extras are already among the 78, so they are not subtracted again. Both 91-character chunks are flagged: S02 chunk 84 is held with its affected page, while S03 chunk 142 is retained with a context restriction. The quarantine file preserves the original text for repair and audit.

The clean JSONL and PKL are reloaded and compared for text and metadata equality. Their 90 records have distinct normalised hashes. All inherited warnings remain attached; `week4_status` describes the new disposition without overwriting Topic 3's status. `approved_for_automatic_retrieval=false` is present on every retained record. The clean file is a controlled manual-reference corpus, not blanket approval for automated answers.

S03 page 4 reports 4,433 study records, while the pinned UCI release contains 4,424. I keep both statements tied to their own versions instead of editing one to match the other. Neither exact hashing nor matching file counts resolves that difference. The table's value-range and approved-versus-enrolled checks pass, but they do not establish that original records contain no measurement errors.

## 4. Representation, Coverage, and Bias Assessment

Adequate coverage is defined by the required tasks, not equal numbers of chunks:

| Required area | Expected authoritative evidence | Actual evidence | Gap / decision |
|---|---|---|---|
| Dataset and outcome definitions | UCI release documentation and its descriptor | S01 has 4,424 rows; S02 describes the dataset; S03 page 4 defines its study outcomes | Supported for a benchmark, subject to the documented release difference |
| T0/T1 feature timing | Source definitions separating enrolment and first-semester attributes | Existing Topic 3 allowlists; source tables distinguish the timepoints | Detailed descriptor extraction is partly quarantined. Use the original tables and keep ambiguous fields excluded |
| Phased prediction interpretation | A cited study describing prediction phases and limitations | S03 provides 60 retained chunks | Study results are context, not our measured results or proof of causal benefit |
| Subgroup audit feasibility | Recorded group variables and sufficient later test denominators | Aggregate gender and age counts below | Full-dataset support cannot guarantee test-set support; no fairness score yet |
| UTM deployment / current student advice | Local authorised data and current institutional validation | None supplied | Outside V1 scope. Do not make these claims |

| source_id | role | input_chunks | retained_chunks | quarantined_chunks | retained_percent |
| --- | --- | --- | --- | --- | --- |
| S02 | Dataset descriptor | 108 | 30 | 78 | 33.33 |
| S03 | Phased prediction study | 60 | 60 | 0 | 66.67 |

![Source coverage and extraction holds](week4_coverage_by_source.png)

Originally S02 contributes 108/168 chunks (64.29%) and S03 contributes 60/168 (35.71%). After quarantine, S02 contributes 30/90 (33.33%) and S03 contributes 60/90 (66.67%). These are different document roles and lengths. The change reflects an extraction intervention; it is not a demographic fairness result.

The least secure **in-scope** area is faithful, readily reusable feature-definition text because much of the descriptor is held. More prediction-study chunks would not repair that gap. Current Malaysian applicability is an additional evidence absence, but is outside the declared benchmark scope.

The predictive labels are Graduate 2,209 (49.93%), Dropout 1,421 (32.12%) and Enrolled 794 (17.95%). The domain grouping below uses recorded gender and the age bands already specified in Topic 2, without inferring new identity attributes.

| grouping | group | records | dropout | non_dropout | percent |
| --- | --- | --- | --- | --- | --- |
| Recorded gender | 0: female | 2868 | 720 | 2148 | 64.83 |
| Recorded gender | 1: male | 1556 | 701 | 855 | 35.17 |
| Age at enrolment | 25 or older | 1138 | 631 | 507 | 25.72 |
| Age at enrolment | Under 25 | 3286 | 790 | 2496 | 74.28 |

Only 110 records have a nationality code other than Portuguese; this is a recorded-code count, not a claim about ethnicity or nationality identity beyond the supplied field. The gender coding is limited to the source's two categories. Neither this count nor excluding gender from predictors demonstrates fairness.

| Risk / origin / affected group | Propagation path | Intervention and Topic 8 follow-up |
|---|---|---|
| Historical and representation risk: one Portuguese institutional setting; the paper describes a historical cohort, and Enrolled is the smallest target class. Students outside that setting and smaller classes may be poorly represented. | Source population and selection → imbalanced prepared table and narrow reference evidence → in V1, model fitting and manual evidence selection favour what is available → potentially uneven errors or overgeneralised explanations. If retrieval is added later, the same narrow source set limits what can be retrieved and generated. | Keep the benchmark-only scope; stratify the future split; fit any balancing inside training folds only. Topic 8 must report per-class metrics, group error gaps and uncertainty. External transfer remains untested without suitable new data. |
| Measurement risk: final recorded outcome is a proxy for academic status, not an observed reason for leaving or a semester-one dropout date. Several financial/status timestamps are uncertain. | Institutional definitions and snapshots → labels/feature windows → in V1, learned estimates and guide interpretations → a user could mistake association for cause or retrospective performance for prospective capability. A future retriever could repeat the same misleading interpretation. | Keep three classes and the fixed timing exclusions; state the outcome horizon. Topic 8 tests forbidden fields, disclosure correctness and explanations. It cannot infer causal intervention benefit from this benchmark. |
| Pipeline-induced representation risk: extraction noise inflates S02's count, while a broad quarantine reduces descriptor access. | PDF text layer → duplicated/misordered chunks, followed by a source-skewed retained corpus → later retrieval could over-weight repeated text before cleaning or miss definitions after cleaning → inaccurate or incomplete answers. | Preserve quarantine and lineage; use original pages for manual claims. Before any Topic 7 index, verify claim-level evidence and repair affected text. If a RAG extension is approved, Topic 8 needs source/definition coverage, retrieval recall and citation checks; none is claimed here. |

**Bias reflection:** The first risk originates mainly in the source population; the third is introduced or amplified by extraction and filtering. Both can change the evidence the system sees, but counts alone cannot show whether a final user is treated unfairly. The controls interrupt different points of the chain. System behaviour still requires later evaluation.

## 5. Privacy, Consent, Rights/Access, and Data Governance

| Source | Owner / version / provenance | Rights and access | Collection basis and limitation |
|---|---|---|---|
| S01: UCI Predict Students' Dropout and Academic Success | Realinho, Vieira Martins, Machado and Baptista; UCI public release retrieved 12 November 2026; full SHA-256 retained in the notebook and registry | UCI lists CC BY 4.0. Reuse needs attribution; public availability is not public-domain status. | Secondary use of a published benchmark; no new personal-data collection. Individual consent documentation was not supplied and is N.V.; the licence does not prove it. |
| S02: Realinho et al., Data 7(11), 146 (2022) | Author-owned article; PDF retrieved 5 November 2026; unchanged Lab 2/3 bytes and source hash | PDF first-page notice states CC BY 4.0 | Public research text used with attribution and page locators. Author names/contact details are publication metadata, not student identifiers. |
| S03: Martins et al., Applied Sciences 13(8), 4702 (2023) | Author-owned article; PDF retrieved 5 November 2026; unchanged Lab 2/3 bytes and source hash | PDF licence notice states CC BY 4.0 | Page 4 describes anonymisation by the source researchers. This is their reported process, not an independently verified legal or re-identification assessment. |

The table contains demographic, academic and socioeconomic attributes. No name, email or student-number column is present in the supplied table, but quasi-identifiers and sensitive combinations still need care. Gender and nationality remain audit-only; age remains both a predictor and an audit variable under the existing policy. Unneeded socioeconomic fields are excluded from the model views. There is no linkage to real UTM students, no collection of user feedback, and no external model service receiving the rows.

RAI2 is stricter than the public-source licence: row-level CSVs remain in the local/Colab working area and are excluded from the public repository and submission ZIP prepared here. The notebook publishes aggregate student counts only. The JSONL/PKL outputs contain attributed paper text, not student profiles. Do not upload local student data as a replacement input. Pickle is loaded only when produced by this notebook or verified against the delivered manifest; JSONL is the preferred inspection format.

Project author owns the project copies, version checks and removal decisions. Before every downstream release, compare source hashes and review source notices. A changed source must receive a new inventory entry and a rerun; never silently overwrite the benchmark version. Keep attributed sources, reports and manifests through assessment and appeals, then review retained copies and remove unnecessary local row-level caches within 30 days after that period ends. The institution's exact assessment-retention period is not supplied and must be confirmed. If a rights or privacy concern arises, hold the affected source immediately and review any published derivatives; no removal has been claimed as already performed.

Source references: [UCI dataset and licence](https://archive.ics.uci.edu/dataset/697/predict), [Realinho et al. (2022)](https://doi.org/10.3390/data7110146), [Martins et al. (2023)](https://doi.org/10.3390/app13084702). Source hashes and dates are recorded in the inherited registry. [Pandera's lazy-validation documentation](https://pandera.readthedocs.io/en/stable/lazy_validation.html) supports the validation method, not the substantive quality conclusions.

## 6. Mitigation Plan and Residual Risk

| Issue | Evidence | Action | Owner / timing | Residual risk |
|---|---|---|---|---|
| Misordered and repeated extraction | S02 pages 5–6; 78 flagged records; 9 duplicate extras | Completed: quarantine the inherited affected page set; preserve all original text and metadata. Planned: verify repaired extraction against each original page before release | Project author; before any automatic ingestion or guide claim using affected text | Conservative hold can remove valid material; extraction repair is not yet complete |
| Short passage needs context | S03 chunk 142, pages 8–9 | Completed: retain with boundary-context flag; check adjacent pages before use | Project author; each relevant guide claim | Other unsampled fragments may also need context |
| Version mismatch | UCI 4,424 versus S03 study 4,433 | Completed: keep separate provenance and stop on hash change; do not substitute study counts into evaluation | Project author; every rerun | Exact cause of release difference remains N.V. |
| Population and class imbalance | Class and domain-coverage tables | Planned: follow locked split/CV protocol; report group and class supports, errors and intervals | Project author; model development and Topic 8 | Current UTM transferability is unsupported |
| Misinterpreted feature timing or outcome | Fixed T0/T1 policy; uncertain snapshots excluded | Completed: allowlist checks. Planned: enforce input checks and outcome-horizon disclosures in the application | Project author; before and during Topic 8 | Retrospective data do not prove prospective validity |
| Privacy, consent and retention uncertainty | Audit attributes; no individual consent records or local retention policy supplied | Completed: publish aggregate evidence only. Planned: confirm applicable retention period; hold new personal-data collection pending an authorised basis | Project author; before scope expansion and after assessment | No independent source-consent or re-identification audit |

## 7. Impact on Topic 2 Requirements / Evaluation Criteria

FR2 remains supported by the unchanged 8/14-field allowlists and excluded-feature assertions. It could fail if future preparation admits later or uncertain snapshots. FR5 and RAI4 are conditional: all substantive reference-guide claims still need source/page verification, especially where descriptor extraction is held. A passed metadata check is not a completed claim ledger.

FR6, FR7, NFR1 and NFR2 remain **not evaluated**. The later protocol must use the same stratified 80/20 split at seed 42 for both timepoints and training-only five-fold CV. Proposed macro-F1 targets are T0 ≥0.50 and T1 ≥0.65, each at least 0.10 above the majority baseline. Proposed Dropout recall/precision targets are T0 ≥0.65/0.60 and T1 ≥0.75/0.65. Topic 4 does not claim that these targets pass.

RAI1 / E5 remains **not evaluated**. Later test groups require at least 30 actual Dropout cases for recall and 30 non-Dropout cases for FPR, with at least two eligible groups before comparing a gap. The proposed maximum pairwise gap is 0.10. Current full-corpus counts are not those test denominators. An unsupported comparison must be inconclusive, not a pass.

NFR4 is supported at the data stage by pinned inputs, checksums and reload equality; repeated model metrics within 0.000001 remain a later requirement. NFR5 is respected in this lab through zero model API calls and no paid inference. RAI2 publication boundaries are maintained. RAI3 prevents interpreting this quality gate as deployment approval or an automated decision about a real student. No latency, SHAP-fidelity or system control-test result is invented.

## 8. Topic 4 Quality Gate Decision

**GO WITH CONDITIONS** for the offline benchmark project and source-checked manual reference work.

The structural checks pass, versions are pinned, table roles are preserved, exact duplicate occurrences are documented, and questionable extraction is separated. This is sufficient to continue model-selection planning using the existing table policy.

Conditions: keep all 78 held paper records outside downstream ingestion; check the original PDF and adjacent-page context for each substantive guide claim; keep student rows private; retain the unchanged feature exclusions; and carry the stated representation and governance limits into later evaluation. Project author owns these follow-ups before the relevant downstream use.

**Automatic ingestion of the held extraction is HOLD.** The retained corpus also has no automatic-retrieval approval until claim/source checks and a scope decision are completed. If a later Topic 7 retrieval exercise is undertaken, it must start from the reviewed Topic 4 corpus and respect these flags, rather than silently using the original Topic 3 text. Topic 8 is where final model behaviour and applicable fairness criteria must be assessed.
