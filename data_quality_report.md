# Data Quality Report — PharmEasy Regional Pulse

## Data Quality Dimensions and Implemented Fixes

| Data-quality dimension | Specific fix implemented |
|---|---|
| Accuracy | Missing `profit_inr` values were imputed using the category-specific mean profit margin calculated from non-missing rows, then multiplied by `sales_inr` and rounded to 2 decimals. |
| Completeness | Missing `category` values were imputed using the deterministic product-to-category lookup built from non-missing rows. |
| Consistency | The `region` column was normalized by stripping leading/trailing whitespace and applying title case, mapping raw variants to the canonical region names. |
| Timeliness | The original `order_date` values were retained so each order remains associated with its April, May, or June 2026 reporting period. |
| Validity | `validate_schema()` checks that all eight required columns are present and returns `validated` for the clean dataset or `blocked_schema` when a required column is missing. |
| Uniqueness | Exact duplicate rows were removed using all eight columns as the duplicate definition. Exactly 59 duplicate rows were removed. |
| Relevance | The cleaning process preserves the fields required for the downstream regional sales, profit, order-count, category, and monthly analysis. |

## Cleaning Results

- Raw rows: 2,159
- Exact duplicate rows removed: 59
- Final clean rows: 2,100
- Missing `category` values before imputation: 48
- Missing `category` values after imputation: 0
- Missing `profit_inr` values before imputation: 94
- Missing `profit_inr` values after imputation: 0
- Canonical active regions after normalization: 9

## Schema Validation

The clean 2,100-row dataset returned:

```text
status: validated
row_count: 2100
missing_columns: []