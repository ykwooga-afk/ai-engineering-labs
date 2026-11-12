# Week 3 Preparation Decisions — Part B

**Student:** Woo Yong Kang | A24AI0123

## B1. Selected pathways

Pathway B prepares the actual UCI benchmark for FR2. Pathway A prepares the two existing domain PDFs for FR5. These branches remain separate. Other modalities and model integration are outside this work.

## B2–B3. Comparison and choice

| Branch | Baseline | Selected preparation | Observed evidence | Benefit / accepted limitation |
|---|---|---|---|---|
| Table | Parsed source without cleanup | Trim whitespace; quarantine exact repeats and conflicting labels | 4,424 → 4,424 rows; 1 header corrected; 0 text cells changed; 0 rows quarantined | Stable schema; no fabricated cleaning or fitted preprocessing. This release does not exercise duplicate-removal outcomes. |
| S02 PDF | Whole-document fixed 1,000-character slices | Page-aware paragraph/line packing, max 1,000 characters, no overlap | 96 baseline vs 108 selected chunks; cross-page chunks 16 → 0 | Exact page location; page breaks and line boundaries may still interrupt meaning. Table extraction remains unverified. |
| S03 PDF | Whole-document fixed 1,000-character slices | Page-aware paragraph/line packing, max 1,000 characters, no overlap | 51 baseline vs 60 selected chunks; cross-page chunks 14 → 0 | Exact page location; page breaks and line boundaries may still interrupt meaning. Table extraction remains unverified. |

The same cleaned content and size cap are used for both document candidates. Baseline and selected counts come from actual execution. Neither chunking approach is semantic chunking. Sample excerpts and counts are in `evidence/document_comparison.json`.

## Predictor policy and data leakage

T0 has 8 conservative predictors; T1 has 14. See `week3_feature_policy.csv` for every raw column. `feature_allowlists.json` names the exact predictor columns; `row_id` is solely a join key.
All second-semester fields, target, technical ID, gender and nationality are excluded from predictor allowlists. Debtor, tuition-fee, scholarship and annual macroeconomic snapshots remain excluded pending time-cutoff verification. Other socioeconomic fields are retained in staging but are not selected in the conservative V1.
The complete staging CSV intentionally retains source information for audit. Downstream training must load the explicit T0/T1 views and allowlists, never automatically use every staging column.
No split, statistical imputation, scaling, encoding, balancing, model fitting or threshold optimisation is performed. Future work must use the common split and training-fold-only fitting from Week 2.

## B3. Validation evidence

37 content/provenance checks passed. Prepared rows: 4,424; quarantined rows: 0; PDF chunks: 168; covered PDF pages: 32.
Checks include read-back equality, row accounting, exact predictor allowlists, target/audit alignment, basic ranges, unique chunk IDs, full cleaned-page content coverage, exact chunk offsets and source/output hashes. Header-only quarantine CSV is a valid zero-row result, not evidence that bad rows were removed.
PASS means these specific checks succeeded; it is not a source-rights, fairness, model-quality or deployment certification.

## B4. Metadata and lineage

The common manifest contains 10 source-to-output mappings. It records source and output SHA-256, attribution/licence, source version, processing, configuration descriptions and provenance limitations. S02 and S03 each map to their selected records within the combined `prepared_text.jsonl`.
The PDF chunk records retain source URL, source hash, page, cleaned-page offsets and a stable record ID. All are marked `candidate_for_manual_review`; an excerpt is not automatically a verified reference-guide claim.

## Saved outputs

- `data/processed/prepared_table.csv`: complete staging table plus internal row key.
- `features_t0.csv`, `features_t1.csv`: predictor views plus join key.
- `targets.csv`, `audit_attributes.csv`: separate outcomes and demographic audit fields.
- `quarantined_rows.csv`: rejected/repeated row log; zero rows for this release.
- `feature_allowlists.json`: exact allowed predictor names.
- `prepared_text.jsonl`: page-linked candidate text from both PDFs.
- `data/week3_manifest.json`: common Part B lineage; not Part C run evidence.

## Remaining work

Run and save the notebook in Google Colab if the current execution environment is local. Part C workflow integration, diagram and decisions are supplied with the complete Week 3 package; see the project README for commit evidence. Topic 4 should review PDF extraction, feature timing, representativeness and data quality. Model-level Week 2 criteria have not been evaluated.
