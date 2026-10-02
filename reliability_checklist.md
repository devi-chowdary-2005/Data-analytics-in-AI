# Reliability Checklist

## 1. Data Reliability

- [x] Raw data was cleaned before analysis.
- [x] Exact duplicate rows were removed.
- [x] Region names were normalized to canonical values.
- [x] Missing category values were imputed using product-category mapping.
- [x] Missing profit values were imputed using category-level mean profit margins.
- [x] Required schema columns were validated.
- [x] Zero-order regions were preserved through the regions master table.

## 2. Metric Reliability

- [x] Regional monthly sales were calculated using SQL GROUP BY.
- [x] Month-on-Month percentage change uses the defined formula.
- [x] The operational alert threshold is fixed at 8%.
- [x] Significance uses a strict absolute-change rule: abs(MoM) > 8%.
- [x] Previous-period state is persisted in `previous_state.json`.
- [x] Reloaded state was checked before calculating the next transition.

## 3. Insight and Recommendation Reliability

- [x] CII output contains one block per unique flagged region.
- [x] A region flagged in multiple transitions is combined into one CII block.
- [x] Guntur's April → May and May → June movements are both represented.
- [x] Numerical claims in the recommendation memo are traceable to calculated metrics.
- [x] Possible external causes are treated as hypotheses rather than established facts.
- [x] Recommendations require human review before operational action.

## 4. Human Review and Auditability

- [x] Automated output passes through a human review gate.
- [x] Valid review decisions are `approve`, `edit`, and `reject`.
- [x] Invalid review decisions are blocked.
- [x] Reviewer identity is recorded.
- [x] Review timestamp is recorded.
- [x] Reviewer notes are recorded.
- [x] Edited recommendations can be recorded.
- [x] Rejected recommendations require a rejection reason.
- [x] Review decisions are persisted in `audit_log.jsonl`.

## Final Reliability Status

**STATUS: READY FOR DASHBOARD AND PRESENTATION**

The pipeline has completed data cleaning, validation, database loading, metric calculation, CII generation, recommendation drafting, and human review/audit controls.