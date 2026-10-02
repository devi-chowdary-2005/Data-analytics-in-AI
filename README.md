# PharmEasy Regional Pulse

A deterministic data engineering and business intelligence project for
analyzing regional sales movements across April, May, and June 2026.

## 1. Project Objective

The project cleans a supplied regional order dataset, validates its
quality, stores the cleaned data in SQLite, calculates regional
month-on-month sales movements, identifies movements above a fixed 8%
operational-alert threshold, and presents the results through a
Streamlit dashboard.

The workflow is:

RAW DATA → CLEANING → VALIDATION → DATABASE → SQL METRICS → MoM FLAGS →
CII REPORT → HUMAN REVIEW → DASHBOARD

## 2. Deliverables

### Source Code

-   `generate_dataset.py` --- supplied deterministic dataset generator
-   `clean_data.py` --- data cleaning, imputation, normalization, and
    schema validation
-   `build_db.py` --- SQLite database creation
-   `queries.py` --- SQL validation and monthly regional metrics
-   `metrics_engine.py` --- MoM calculations, alert flags, and state
    persistence
-   `draft_report.py` --- CII report generation
-   `review_gate.py` --- human review and audit logging
-   `app.py` --- Streamlit dashboard

### Documentation

-   `data_quality_report.md` --- data quality assessment
-   `memo.md` --- recommendation memo
-   `reliability_checklist.md` --- reliability and readiness checklist
-   `presentation_storyline.md` --- presentation structure and talking
    points
-   `README.md` --- project documentation

### Data and Outputs

-   `pharmeasy_orders_raw.csv` --- generated raw dataset
-   `regions_master.csv` --- region master data
-   `orders_clean.csv` --- cleaned dataset
-   `pharmeasy.db` --- SQLite database
-   `draft_report_output.json` --- generated CII output
-   `previous_state.json` --- persisted metric state
-   `audit_log.jsonl` --- human review record

## 3. Dataset Summary

The generated raw dataset contains:

-   2,159 rows
-   2,100 legitimate order rows
-   59 exact duplicate rows
-   10 master regions
-   9 active order regions
-   1 zero-order region: Kurnool
-   3 reporting months: April, May, and June 2026

The cleaning process produces 2,100 clean order rows.

## 4. Data Quality Controls

The pipeline addresses:

-   Accuracy
-   Completeness
-   Consistency
-   Timeliness
-   Validity
-   Uniqueness
-   Relevance

Missing category values are recovered using the product-to-category
relationship.

Missing profit values are estimated using the mean profit margin of the
corresponding category.

Exact duplicate rows are removed.

Region names are normalized before validation.

The required schema is checked before the cleaned dataset is accepted.

## 5. Metric Definition

Regional monthly sales are calculated using SQL aggregation.

Month-on-month change is:

`(Current Month Sales - Previous Month Sales) / Previous Month Sales × 100`

A movement is flagged when:

`abs(MoM change) > 8%`

The analysis contains two transitions:

-   April → May 2026
-   May → June 2026

The 8% value is a fixed operational-alert threshold defined for the
project.

For a previous-month value of zero, percentage change is treated as
undefined rather than forcing a misleading percentage.

## 6. Main Example

Guntur is used in the CII and recommendation workflow.

  Month                Sales
  ------------ -------------
  April 2026      ₹62,442.27
  May 2026       ₹138,738.93
  June 2026       ₹99,745.18

MoM movement:

-   April → May: +122.19%
-   May → June: -28.11%

The data supports the size and direction of these movements. It does not
establish an underlying cause.

## 7. Human Review

Recommendations are not treated as final automatically.

`review_gate.py` supports:

1.  Approve
2.  Edit
3.  Reject

The review decision, reviewer, timestamp, and relevant notes are written
to `audit_log.jsonl`.

## 8. Dashboard

The Streamlit dashboard provides:

-   Executive KPIs
-   Monthly sales trend
-   Regional comparison
-   Category mix
-   Regional movement alerts
-   Regional filtering
-   Category detail
-   Product detail
-   Executive summary
-   Methodology

Kurnool remains visible as a zero-order master region where applicable.
Its percentage movement is shown as undefined when the comparison base
is zero.

## 9. How to Run

Install the required packages:

``` bash
pip install pandas streamlit plotly
```

Run the data pipeline in this order:

``` bash
python generate_dataset.py
python clean_data.py
python build_db.py
python queries.py
python metrics_engine.py
python draft_report.py
python review_gate.py
```

The review gate requires a human decision.

Start the dashboard with:

``` bash
python -m streamlit run app.py
```

## 10. Project Structure

``` text
PharmEasy-Regional-Pulse/
├── generate_dataset.py
├── clean_data.py
├── build_db.py
├── queries.py
├── metrics_engine.py
├── draft_report.py
├── review_gate.py
├── app.py
├── data_quality_report.md
├── memo.md
├── reliability_checklist.md
├── presentation_storyline.md
├── README.md
├── pharmeasy_orders_raw.csv
├── regions_master.csv
├── orders_clean.csv
├── pharmeasy.db
├── draft_report_output.json
├── previous_state.json
└── audit_log.jsonl
```

## 11. Design Principles

The project follows a deterministic and traceable workflow.

Calculations are based on the supplied dataset and explicit rules.

External explanations are not presented as facts when they are not
supported by the available data.

Human review is included before recommendations are treated as approved
output.

The dashboard is intended to support investigation and decision-making
rather than replace human judgment.
