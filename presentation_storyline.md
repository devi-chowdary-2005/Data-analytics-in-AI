# PharmEasy Regional Pulse --- Presentation Storyline
project finalized
## 1. Problem

The project analyzes regional sales performance across April, May, and
June 2026 using a deterministic data pipeline.

The objective is to identify meaningful month-on-month movements,
validate the underlying data, and convert the results into reviewable
operational insights.

## 2. Data Pipeline

RAW DATA → CLEANING → VALIDATION → SQLite DATABASE → SQL METRICS → MoM
ANALYSIS → CII REPORT → HUMAN REVIEW → STREAMLIT DASHBOARD

The pipeline removes exact duplicates, standardizes region names, fills
missing category and profit values using defined rules, validates the
schema, stores the cleaned data in SQLite, calculates monthly metrics,
and produces reviewable findings.

## 3. Data Quality

The raw dataset contains 2,159 rows.

The cleaning process removes 59 exact duplicate rows, leaving 2,100
clean order rows.

There are 48 missing category values and 94 missing profit values.
Category values are recovered using the product-to-category
relationship. Missing profit is estimated using the mean profit margin
for the corresponding category.

The master region file contains 10 regions. Kurnool is intentionally
retained as a zero-order region.

## 4. Metric Logic

Monthly sales are calculated by region using SQL GROUP BY operations.

Month-on-month change is calculated as:

(Current Month Sales - Previous Month Sales) / Previous Month Sales ×
100

A region is flagged when the absolute month-on-month change is greater
than 8%.

The analysis covers both:

-   April → May 2026
-   May → June 2026

The 8% threshold is an operational alert rule for this project, not a
statistical significance test.

## 5. Key Finding

Guntur provides the main example used for the CII and recommendation
workflow.

Guntur sales:

-   April 2026: ₹62,442.27
-   May 2026: ₹138,738.93
-   June 2026: ₹99,745.18

The resulting movements are:

-   April → May: +122.19%
-   May → June: -28.11%

The dataset establishes the size and direction of the movements. It does
not establish the underlying business cause.

## 6. CII and Recommendation Workflow

The reporting layer converts flagged movements into CII blocks
containing:

-   Region
-   Time period
-   Sales values
-   Month-on-month change
-   Evidence
-   Interpretation
-   Recommendation
-   Next check

Recommendations are routed through a human review gate before being
treated as approved output.

The review gate supports:

-   Approve
-   Edit
-   Reject

Each review decision is recorded in the audit log.

## 7. Dashboard Story

The Streamlit dashboard presents the analysis at three levels.

### Level 1 --- Executive View

Shows overall KPIs, monthly sales trends, regional comparisons, and the
executive summary.

### Level 2 --- Regional View

Shows regional sales movements and identifies regions crossing the 8%
alert threshold.

### Level 3 --- Detail View

Shows category and product-level information that can be used for
follow-up investigation.

The regional filter connects the regional and detailed views.

## 8. SCR Reframing

### Situation

Regional sales changed materially across the three-month reporting
period.

### Complication

Several regions crossed the fixed 8% month-on-month alert threshold, and
some movements reversed in the following month.

### Resolution

Use the dashboard and order-level/category-level evidence to review
flagged regions, verify the movement, and determine whether operational
follow-up is required.

The system supports the decision; it does not assign a cause that is not
present in the data.

## 9. OCD Reframing

### Observe

Review regional sales, monthly changes, category mix, and product-level
activity.

### Compare

Compare the flagged month with the previous month and then compare the
following month to determine whether the movement continues or reverses.

### Decide

Route material movements for human review before operational action.

## 10. Anticipated Pushback

### Q1. Why was Guntur flagged?

Acknowledge: The movement is large and clearly exceeds the project's 8%
alert threshold.

Response: Guntur increased by 122.19% from April to May and then
decreased by 28.11% from May to June. The next step is to inspect
order-level and category-level data before deciding what caused the
movement.

### Q2. Can we say the increase was caused by a promotion or competitor activity?

Acknowledge: Those are possible business explanations.

Response: The available dataset does not contain evidence establishing
those causes. They should be treated as hypotheses and checked against
additional business information before being presented as facts.

## 11. Closing

The final deliverable combines data quality controls, SQL analysis,
deterministic metrics, reviewable recommendations, auditability, and an
interactive dashboard.

The main principle is traceability: every reported movement should be
connected back to the underlying data and calculation.
