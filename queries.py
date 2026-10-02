"""
queries.py
PharmEasy Regional Pulse — Part 2

Task 2.2 — JOIN validation
Task 2.3 — Region x Month metrics and MoM growth
"""
# Dharmavaram
import sqlite3


DATABASE_FILE = "pharmeasy.db"


# ============================================================
# Connect to database
# ============================================================

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()


# ============================================================
# TASK 2.2
# JOIN validation
# ============================================================

# ------------------------------------------------------------
# 1. LEFT JOIN vs INNER JOIN row count
# ------------------------------------------------------------

left_join_query = """
SELECT COUNT(*)
FROM regions_master r
LEFT JOIN orders_clean o
    ON r.region = o.region;
"""

inner_join_query = """
SELECT COUNT(*)
FROM regions_master r
INNER JOIN orders_clean o
    ON r.region = o.region;
"""

cursor.execute(left_join_query)
left_count = cursor.fetchone()[0]

cursor.execute(inner_join_query)
inner_count = cursor.fetchone()[0]

print("========================================")
print("TASK 2.2 — JOIN VALIDATION")
print("========================================")

print("\n1. LEFT JOIN vs INNER JOIN")
print(f"LEFT JOIN row count : {left_count}")
print(f"INNER JOIN row count: {inner_count}")
print(f"Difference          : {left_count - inner_count}")


# ------------------------------------------------------------
# 2. Duplicate order_id check
# ------------------------------------------------------------

duplicate_query = """
SELECT order_id, COUNT(*) AS order_count
FROM orders_clean
GROUP BY order_id
HAVING COUNT(*) > 1;
"""

cursor.execute(duplicate_query)
duplicate_rows = cursor.fetchall()

print("\n2. Duplicate order_id check")

if duplicate_rows:
    print("Duplicate order_ids found:")
    for row in duplicate_rows:
        print(row)
else:
    print("Duplicate order_ids: 0 rows")


# ------------------------------------------------------------
# 3. COUNT(*) vs COUNT(o.order_id)
# ------------------------------------------------------------

null_check_query = """
SELECT
    r.region,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM regions_master r
LEFT JOIN orders_clean o
    ON r.region = o.region
GROUP BY r.region
ORDER BY r.region;
"""

cursor.execute(null_check_query)
null_check_rows = cursor.fetchall()

print("\n3. COUNT(*) vs COUNT(o.order_id)")
print(
    f"{'Region':<15}"
    f"{'COUNT(*)':<12}"
    f"{'COUNT(order_id)':<18}"
)

for region, count_star, count_order_id in null_check_rows:
    print(
        f"{region:<15}"
        f"{count_star:<12}"
        f"{count_order_id:<18}"
    )


# ------------------------------------------------------------
# 4. Per-region order counts
# ------------------------------------------------------------

region_count_query = """
SELECT
    r.region,
    COUNT(o.order_id) AS order_count
FROM regions_master r
LEFT JOIN orders_clean o
    ON r.region = o.region
GROUP BY r.region
ORDER BY order_count ASC;
"""

cursor.execute(region_count_query)
region_count_rows = cursor.fetchall()

print("\n4. Per-region order counts")
print(
    f"{'Region':<15}"
    f"{'Order Count':<12}"
)

for region, order_count in region_count_rows:
    print(
        f"{region:<15}"
        f"{order_count:<12}"
    )


# ============================================================
# TASK 2.3
# Region × Month sales and MoM growth
# ============================================================

print("\n\n========================================")
print("TASK 2.3 — REGION × MONTH METRICS")
print("========================================")


# ------------------------------------------------------------
# Step 1 — Calculate total sales per region per month
# using SQL GROUP BY
# ------------------------------------------------------------

monthly_sales_query = """
SELECT
    region,
    substr(order_date, 1, 7) AS month,
    ROUND(SUM(sales_inr), 2) AS total_sales_inr
FROM orders_clean
GROUP BY
    region,
    substr(order_date, 1, 7)
ORDER BY
    region,
    month;
"""

cursor.execute(monthly_sales_query)
monthly_sales_rows = cursor.fetchall()


print("\nMonthly sales:")

print(
    f"{'Region':<15}"
    f"{'Month':<12}"
    f"{'Sales (INR)':<15}"
)

for region, month, sales in monthly_sales_rows:
    print(
        f"{region:<15}"
        f"{month:<12}"
        f"{sales:<15.2f}"
    )


# ------------------------------------------------------------
# Step 2 — Store monthly sales in a dictionary
# ------------------------------------------------------------

monthly_sales = {}

for region, month, sales in monthly_sales_rows:

    if region not in monthly_sales:
        monthly_sales[region] = {}

    monthly_sales[region][month] = sales


# ------------------------------------------------------------
# Step 3 — Calculate MoM growth
#
# Formula:
#
# ((Current Month - Previous Month)
#      / Previous Month) × 100
# ------------------------------------------------------------

def calculate_mom_growth(current_month, previous_month):
    """
    Calculate Month-over-Month percentage growth.

    If previous month is zero, return 0.
    """

    if previous_month == 0:
        return 0

    return (
        (current_month - previous_month)
        / previous_month
    ) * 100


print("\nMoM growth:")
print(
    f"{'Region':<15}"
    f"{'Apr → May':<15}"
    f"{'May → Jun':<15}"
)

mom_changes = {}

for region in sorted(monthly_sales.keys()):

    april = monthly_sales[region].get("2026-04", 0)
    may = monthly_sales[region].get("2026-05", 0)
    june = monthly_sales[region].get("2026-06", 0)

    april_may = calculate_mom_growth(may, april)
    may_june = calculate_mom_growth(june, may)

    mom_changes[region] = {
        "April": april,
        "May": may,
        "June": june,
        "April_to_May": april_may,
        "May_to_June": may_june
    }

    print(
        f"{region:<15}"
        f"{april_may:>10.2f}%"
        f"{may_june:>15.2f}%"
    )


# ============================================================
# Close database
# ============================================================

connection.close()
