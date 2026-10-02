"""
metrics_engine.py
PharmEasy Regional Pulse — Task 2.4

Implements:
1. compute_percentage_change_v1(current, previous)
2. flag_significant_regions_v1(changes, threshold=8)
3. save_state_v1(month_summary, path)
4. load_previous_state_v1(path)

Task 2.4 also demonstrates:
- April -> May significance flagging
- May -> June significance flagging
- April state persistence
"""
final review october 2026 verified
import json
import os


# ============================================================
# 1. PERCENTAGE CHANGE
# ============================================================

def compute_percentage_change_v1(current, previous):
    """
    Calculate Month-on-Month percentage change.

    Formula:
        ((current - previous) / previous) * 100

    If previous is zero, return 0 to avoid division-by-zero.
    """

    if previous == 0:
        return 0

    return ((current - previous) / previous) * 100


# ============================================================
# 2. SIGNIFICANT REGION FLAGGING
# ============================================================

def flag_significant_regions_v1(changes, threshold=8):
    """
    Flag regions where the absolute MoM change exceeds
    the supplied threshold.

    Important:
        abs(change) > threshold

    Therefore:
        +8.00%  -> NOT flagged
        -8.00%  -> NOT flagged
        +8.01%  -> flagged
        -8.01%  -> flagged
    """

    flagged = []

    for region, change in changes.items():
        if abs(change) > threshold:
            flagged.append(region)

    return flagged


# ============================================================
# 3. SAVE STATE
# ============================================================

def save_state_v1(month_summary, path):
    """
    Save a month's computed summary as JSON.
    """

    with open(path, "w", encoding="utf-8") as f:
        json.dump(month_summary, f, indent=2)


# ============================================================
# 4. LOAD PREVIOUS STATE
# ============================================================

def load_previous_state_v1(path):
    """
    Load a previously saved monthly summary.

    If the file does not exist, return an empty dictionary.
    """

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# TEST / DEMONSTRATION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("TASK 2.4 — SIGNIFICANCE FLAGGING WITH STATE PERSISTENCE")
    print("=" * 60)

    # --------------------------------------------------------
    # TEST 1 — Percentage change
    # --------------------------------------------------------

    print("\n1. Percentage change tests")
    print("-" * 60)

    result = compute_percentage_change_v1(122.19, 100)

    print(
        "Current = 122.19, Previous = 100:",
        round(result, 2),
        "%"
    )

    zero_result = compute_percentage_change_v1(100, 0)

    print(
        "Current = 100, Previous = 0:",
        zero_result,
        "%"
    )


    # --------------------------------------------------------
    # APRIL DATA
    # --------------------------------------------------------

    april_sales = {
        "Bengaluru": 203505.48,
        "Guntur": 62442.27,
        "Hyderabad": 209670.15,
        "Karimnagar": 49815.71,
        "Nellore": 85623.19,
        "Tirupati": 54582.74,
        "Vijayawada": 171334.19,
        "Visakhapatnam": 134765.29,
        "Warangal": 100468.14,
    }


    # --------------------------------------------------------
    # MAY DATA
    # --------------------------------------------------------

    may_sales = {
        "Bengaluru": 172929.68,
        "Guntur": 138738.93,
        "Hyderabad": 243825.28,
        "Karimnagar": 61585.90,
        "Nellore": 91184.86,
        "Tirupati": 91083.20,
        "Vijayawada": 174863.57,
        "Visakhapatnam": 50590.08,
        "Warangal": 78339.23,
    }


    # --------------------------------------------------------
    # JUNE DATA
    # --------------------------------------------------------

    june_sales = {
        "Bengaluru": 170294.11,
        "Guntur": 99745.18,
        "Hyderabad": 294088.56,
        "Karimnagar": 34490.58,
        "Nellore": 94393.62,
        "Tirupati": 75530.99,
        "Vijayawada": 153849.68,
        "Visakhapatnam": 100735.57,
        "Warangal": 66715.24,
    }


    # ========================================================
    # APRIL -> MAY
    # ========================================================

    print("\n2. April -> May MoM changes")
    print("-" * 60)

    april_may_changes = {}

    for region in april_sales:

        change = compute_percentage_change_v1(
            may_sales[region],
            april_sales[region]
        )

        april_may_changes[region] = change

        print(
            f"{region:15} "
            f"{change:8.2f}%"
        )


    flagged_april_may = flag_significant_regions_v1(
        april_may_changes,
        threshold=8
    )


    print("\nApril -> May flagged regions:")

    for region in flagged_april_may:
        print(" -", region)

    print(
        "\nNumber of flagged regions:",
        len(flagged_april_may)
    )


    # ========================================================
    # MAY -> JUNE
    # ========================================================

    print("\n3. May -> June MoM changes")
    print("-" * 60)

    may_june_changes = {}

    for region in may_sales:

        change = compute_percentage_change_v1(
            june_sales[region],
            may_sales[region]
        )

        may_june_changes[region] = change

        print(
            f"{region:15} "
            f"{change:8.2f}%"
        )


    flagged_may_june = flag_significant_regions_v1(
        may_june_changes,
        threshold=8
    )


    print("\nMay -> June flagged regions:")

    for region in flagged_may_june:
        print(" -", region)

    print(
        "\nNumber of flagged regions:",
        len(flagged_may_june)
    )


    # ========================================================
    # STATE PERSISTENCE
    # ========================================================

    print("\n4. State persistence test")
    print("-" * 60)

    state_file = "previous_state.json"


    # Save the complete April summary.
    # This is the summary used as the previous month
    # when calculating April -> May growth.

    april_summary = {
        "month": "2026-04",
        "sales_by_region": april_sales
    }


    save_state_v1(
        april_summary,
        state_file
    )


    print("Saved April state:")
    print(april_summary)


    # Load the state back.

    loaded_april_state = load_previous_state_v1(
        state_file
    )


    print("\nLoaded April state:")
    print(loaded_april_state)


    # Verify that the loaded dictionary is identical
    # to the dictionary that was saved.

    if loaded_april_state == april_summary:

        print("\nState persistence test: PASSED")

    else:

        print("\nState persistence test: FAILED")


    # ========================================================
    # VERIFY NELLORE IS NEVER FLAGGED
    # ========================================================

    print("\n5. Nellore baseline verification")
    print("-" * 60)

    nellore_april_may = april_may_changes["Nellore"]
    nellore_may_june = may_june_changes["Nellore"]

    print(
        f"Nellore April -> May: "
        f"{nellore_april_may:.2f}%"
    )

    print(
        f"Nellore May -> June: "
        f"{nellore_may_june:.2f}%"
    )


    if (
        "Nellore" not in flagged_april_may
        and
        "Nellore" not in flagged_may_june
    ):

        print("Nellore flag check: PASSED")

    else:

        print("Nellore flag check: FAILED")


    # ========================================================
    # FINAL ACCEPTANCE CHECK
    # ========================================================

    print("\n" + "=" * 60)
    print("TASK 2.4 ACCEPTANCE CHECK")
    print("=" * 60)

    expected_april_may = {
        "Hyderabad",
        "Warangal",
        "Visakhapatnam",
        "Guntur",
        "Tirupati",
        "Karimnagar",
        "Bengaluru"
    }

    expected_may_june = {
        "Hyderabad",
        "Warangal",
        "Vijayawada",
        "Visakhapatnam",
        "Guntur",
        "Tirupati",
        "Karimnagar"
    }


    actual_april_may = set(flagged_april_may)
    actual_may_june = set(flagged_may_june)


    if actual_april_may == expected_april_may:
        print("April -> May flagging: PASSED")
    else:
        print("April -> May flagging: FAILED")


    if actual_may_june == expected_may_june:
        print("May -> June flagging: PASSED")
    else:
        print("May -> June flagging: FAILED")


    if loaded_april_state == april_summary:
        print("April state persistence: PASSED")
    else:
        print("April state persistence: FAILED")


    if (
        actual_april_may == expected_april_may
        and
        actual_may_june == expected_may_june
        and
        loaded_april_state == april_summary
    ):

        print("\nTASK 2.4: PASSED")
        print("=" * 60)

    else:

        print("\nTASK 2.4: CHECK REQUIRED")
        print("=" * 60)
