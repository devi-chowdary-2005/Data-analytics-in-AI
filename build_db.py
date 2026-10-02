"""
build_db.py
PharmEasy Regional Pulse — Task 2.1

Loads:
    regions_master.csv
    orders_clean.csv

into:
    pharmeasy.db

Tables:
    regions_master
    orders_clean
"""

import sqlite3
import pandas as pd


# ============================================================
# File names
# ============================================================

REGIONS_FILE = "regions_master.csv"
ORDERS_FILE = "orders_clean.csv"
DATABASE_FILE = "pharmeasy.db"


# ============================================================
# Load CSV files
# ============================================================

regions_df = pd.read_csv(REGIONS_FILE)
orders_df = pd.read_csv(ORDERS_FILE)

print(f"Regions loaded: {len(regions_df)}")
print(f"Clean orders loaded: {len(orders_df)}")


# ============================================================
# Basic validation before creating database
# ============================================================

if len(regions_df) != 10:
    raise ValueError(
        f"Expected 10 regions, got {len(regions_df)}"
    )

if len(orders_df) != 2100:
    raise ValueError(
        f"Expected 2100 clean orders, got {len(orders_df)}"
    )


# ============================================================
# Create SQLite database
# ============================================================

connection = sqlite3.connect(DATABASE_FILE)


# ============================================================
# Write tables
# ============================================================

regions_df.to_sql(
    "regions_master",
    connection,
    if_exists="replace",
    index=False
)

orders_df.to_sql(
    "orders_clean",
    connection,
    if_exists="replace",
    index=False
)


# ============================================================
# Verify database contents
# ============================================================

cursor = connection.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM regions_master"
)
region_count = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM orders_clean"
)
order_count = cursor.fetchone()[0]


print("\nDatabase created successfully.")
print(f"Database: {DATABASE_FILE}")
print(f"regions_master rows: {region_count}")
print(f"orders_clean rows: {order_count}")


# ============================================================
# Close database
# ============================================================

connection.close()