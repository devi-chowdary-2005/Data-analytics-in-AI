import pandas as pd


def validate_schema(df, required_columns):
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        status = "blocked_schema"
    else:
        status = "validated"

    return {
        "status": status,
        "row_count": len(df),
        "missing_columns": missing_columns
    }


RAW_FILE = "pharmeasy_orders_raw.csv"
MASTER_FILE = "regions_master.csv"
OUTPUT_FILE = "orders_clean.csv"

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "region",
    "category",
    "product",
    "quantity",
    "sales_inr",
    "profit_inr"
]


df = pd.read_csv(RAW_FILE, dtype=str)

print(f"Raw rows loaded: {len(df)}")


df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["sales_inr"] = pd.to_numeric(df["sales_inr"], errors="coerce")
df["profit_inr"] = pd.to_numeric(df["profit_inr"], errors="coerce")


before_dedup = len(df)

df = df.drop_duplicates(keep="first").copy()

duplicates_removed = before_dedup - len(df)

print(f"Exact duplicate rows removed: {duplicates_removed}")
print(f"Rows after deduplication: {len(df)}")


df["region"] = (
    df["region"]
    .astype(str)
    .str.strip()
    .str.title()
)


regions_master = pd.read_csv(MASTER_FILE)

active_regions = (
    regions_master.loc[
        regions_master["region"] != "Kurnool",
        "region"
    ]
    .tolist()
)

invalid_regions = sorted(
    set(df["region"].dropna()) - set(active_regions)
)

if invalid_regions:
    raise ValueError(
        f"Unexpected region names after normalization: {invalid_regions}"
    )

print(f"Canonical active regions: {df['region'].nunique()}")


missing_category_before = df["category"].isna().sum()

print(f"Missing category values before: {missing_category_before}")


product_category_lookup = {}

non_missing_category_rows = df[
    df["category"].notna()
    & (df["category"].astype(str).str.strip() != "")
]

for _, row in non_missing_category_rows.iterrows():

    product = row["product"]
    category = row["category"]

    if product in product_category_lookup:
        if product_category_lookup[product] != category:
            raise ValueError(
                f"Product '{product}' maps to multiple categories."
            )
    else:
        product_category_lookup[product] = category


def fill_category(row):
    if pd.isna(row["category"]) or str(row["category"]).strip() == "":
        product = row["product"]

        if product not in product_category_lookup:
            raise ValueError(
                f"No category found for product: {product}"
            )

        return product_category_lookup[product]

    return row["category"]


df["category"] = df.apply(fill_category, axis=1)

missing_category_after = df["category"].isna().sum()

print(
    f"Missing category values imputed: "
    f"{missing_category_before - missing_category_after}"
)

print(
    f"Missing category values remaining: "
    f"{missing_category_after}"
)


missing_profit_before = df["profit_inr"].isna().sum()

print(f"Missing profit values before: {missing_profit_before}")


df["profit_margin"] = df["profit_inr"] / df["sales_inr"]

category_mean_margin = (
    df.loc[
        df["profit_inr"].notna(),
        ["category", "profit_margin"]
    ]
    .groupby("category")["profit_margin"]
    .mean()
)


def fill_profit(row):

    if pd.isna(row["profit_inr"]):

        category = row["category"]

        if category not in category_mean_margin:
            raise ValueError(
                f"No mean profit margin found for category: {category}"
            )

        margin = category_mean_margin[category]

        return round(row["sales_inr"] * margin, 2)

    return row["profit_inr"]


df["profit_inr"] = df.apply(fill_profit, axis=1)

df = df.drop(columns=["profit_margin"])

missing_profit_after = df["profit_inr"].isna().sum()

print(
    f"Missing profit values imputed: "
    f"{missing_profit_before - missing_profit_after}"
)

print(
    f"Missing profit values remaining: "
    f"{missing_profit_after}"
)


if len(df) != 2100:
    raise ValueError(
        f"Expected 2100 clean rows, got {len(df)}"
    )

if missing_category_after != 0:
    raise ValueError(
        "Some category values are still missing."
    )

if missing_profit_after != 0:
    raise ValueError(
        "Some profit values are still missing."
    )


df.to_csv(OUTPUT_FILE, index=False)


print("\nCleaning completed successfully.")
print(f"Clean dataset saved to: {OUTPUT_FILE}")
print(f"Final clean rows: {len(df)}")


clean_result = validate_schema(
    df,
    REQUIRED_COLUMNS
)

print("\n========================================")
print("Task 1.3 — Clean Dataset Validation")
print("========================================")

print(f"Status: {clean_result['status']}")
print(f"Row count: {clean_result['row_count']}")
print(f"Missing columns: {clean_result['missing_columns']}")


broken_df = df.drop(columns=["profit_inr"])

broken_result = validate_schema(
    broken_df,
    REQUIRED_COLUMNS
)

print("\n========================================")
print("Task 1.3 — Broken Dataset Validation")
print("========================================")

print(f"Status: {broken_result['status']}")
print(f"Row count: {broken_result['row_count']}")
print(f"Missing columns: {broken_result['missing_columns']}")