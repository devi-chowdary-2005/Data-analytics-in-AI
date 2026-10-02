"""
draft_report.py
PharmEasy Regional Pulse — Task 3.1

Creates one Context-Insight-Implication (CII) block
for every unique region flagged in Part 2.
"""
# CII logic - final validated implementation
import json


# ============================================================
# TASK 3.1 — CII REPORT GENERATOR
# ============================================================

def draft_report_v1(flagged_regions, metrics):
    """
    Create one CII block per unique flagged region.

    flagged_regions:
        Can contain regions from April->May and May->June.
        Duplicate regions are combined into one block.

    metrics:
        Dictionary containing monthly sales and MoM changes.
    """

    # Remove duplicate regions while preserving order.
    unique_regions = list(dict.fromkeys(flagged_regions))

    report = []

    for region in unique_regions:

        april_sales = metrics["sales"]["2026-04"].get(region, 0)
        may_sales = metrics["sales"]["2026-05"].get(region, 0)
        june_sales = metrics["sales"]["2026-06"].get(region, 0)

        april_may_change = metrics["changes"]["2026-04_to_2026-05"].get(
            region, 0
        )

        may_june_change = metrics["changes"]["2026-05_to_2026-06"].get(
            region, 0
        )

        # Determine which transitions flagged the region.
        flagged_transitions = []

        if region in metrics["flagged"]["2026-04_to_2026-05"]:
            flagged_transitions.append("April → May")

        if region in metrics["flagged"]["2026-05_to_2026-06"]:
            flagged_transitions.append("May → June")

        # ----------------------------------------------------
        # Context
        # ----------------------------------------------------

        context = (
            f"{region} recorded sales of "
            f"₹{april_sales:,.2f} in April 2026, "
            f"₹{may_sales:,.2f} in May 2026, and "
            f"₹{june_sales:,.2f} in June 2026."
        )

        # ----------------------------------------------------
        # Insight
        # ----------------------------------------------------

        if len(flagged_transitions) == 2:

            insight = (
                f"The region crossed the 8% operational-alert threshold "
                f"in both monitored transitions: "
                f"April → May changed by {april_may_change:.2f}% "
                f"and May → June changed by {may_june_change:.2f}%."
            )

        elif "April → May" in flagged_transitions:

            insight = (
                f"The April → May sales change was "
                f"{april_may_change:.2f}%, exceeding the "
                f"8% operational-alert threshold."
            )

        else:

            insight = (
                f"The May → June sales change was "
                f"{may_june_change:.2f}%, exceeding the "
                f"8% operational-alert threshold."
            )

        # ----------------------------------------------------
        # Implication
        # ----------------------------------------------------

        implication = (
            "The change should receive a human review before "
            "any operational action is taken; the percentage "
            "threshold is an alert rule rather than proof of a "
            "specific underlying cause."
        )

        # ----------------------------------------------------
        # Store CII block
        # ----------------------------------------------------

        report.append({
            "region": region,
            "flagged_transitions": flagged_transitions,
            "Context": context,
            "Insight": insight,
            "Implication": implication
        })

    return report


# ============================================================
# TEST DATA FROM PART 2
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("TASK 3.1 — CII INSIGHT GENERATOR")
    print("=" * 65)

    # --------------------------------------------------------
    # Sales from Task 2.3
    # --------------------------------------------------------

    sales = {
        "2026-04": {
            "Bengaluru": 203505.48,
            "Guntur": 62442.27,
            "Hyderabad": 209670.15,
            "Karimnagar": 49815.71,
            "Nellore": 85623.19,
            "Tirupati": 54582.74,
            "Vijayawada": 171334.19,
            "Visakhapatnam": 134765.29,
            "Warangal": 100468.14
        },

        "2026-05": {
            "Bengaluru": 172929.68,
            "Guntur": 138738.93,
            "Hyderabad": 243825.28,
            "Karimnagar": 61585.90,
            "Nellore": 91184.86,
            "Tirupati": 91083.20,
            "Vijayawada": 174863.57,
            "Visakhapatnam": 50590.08,
            "Warangal": 78339.23
        },

        "2026-06": {
            "Bengaluru": 170294.11,
            "Guntur": 99745.18,
            "Hyderabad": 294088.56,
            "Karimnagar": 34490.58,
            "Nellore": 94393.62,
            "Tirupati": 75530.99,
            "Vijayawada": 153849.68,
            "Visakhapatnam": 100735.57,
            "Warangal": 66715.24
        }
    }


    # --------------------------------------------------------
    # MoM changes from Task 2.3
    # --------------------------------------------------------

    changes = {

        "2026-04_to_2026-05": {
            "Bengaluru": -15.02,
            "Guntur": 122.19,
            "Hyderabad": 16.29,
            "Karimnagar": 23.63,
            "Nellore": 6.50,
            "Tirupati": 66.87,
            "Vijayawada": 2.06,
            "Visakhapatnam": -62.46,
            "Warangal": -22.03
        },

        "2026-05_to_2026-06": {
            "Bengaluru": -1.52,
            "Guntur": -28.11,
            "Hyderabad": 20.61,
            "Karimnagar": -44.00,
            "Nellore": 3.52,
            "Tirupati": -17.07,
            "Vijayawada": -12.02,
            "Visakhapatnam": 99.12,
            "Warangal": -14.84
        }
    }


    # --------------------------------------------------------
    # Flagged regions from Task 2.4
    # --------------------------------------------------------

    flagged = {

        "2026-04_to_2026-05": [
            "Bengaluru",
            "Guntur",
            "Hyderabad",
            "Karimnagar",
            "Tirupati",
            "Visakhapatnam",
            "Warangal"
        ],

        "2026-05_to_2026-06": [
            "Guntur",
            "Hyderabad",
            "Karimnagar",
            "Tirupati",
            "Vijayawada",
            "Visakhapatnam",
            "Warangal"
        ]
    }


    # --------------------------------------------------------
    # Combine flags from both transitions
    # --------------------------------------------------------

    all_flagged_regions = (
        flagged["2026-04_to_2026-05"]
        + flagged["2026-05_to_2026-06"]
    )


    metrics = {
        "sales": sales,
        "changes": changes,
        "flagged": flagged
    }


    # --------------------------------------------------------
    # Generate report
    # --------------------------------------------------------

    report = draft_report_v1(
        all_flagged_regions,
        metrics
    )


    # --------------------------------------------------------
    # Print report
    # --------------------------------------------------------

    print("\nGenerated CII blocks:")
    print("-" * 65)

    for block in report:

        print(f"\nREGION: {block['region']}")

        print(
            "Flagged transitions:",
            ", ".join(block["flagged_transitions"])
        )

        print("\nContext:")
        print(block["Context"])

        print("\nInsight:")
        print(block["Insight"])

        print("\nImplication:")
        print(block["Implication"])

        print("-" * 65)


    # --------------------------------------------------------
    # Save JSON output
    # --------------------------------------------------------

    with open(
        "draft_report_output.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False
        )


    # --------------------------------------------------------
    # Acceptance checks
    # --------------------------------------------------------

    expected_regions = {
        "Bengaluru",
        "Guntur",
        "Hyderabad",
        "Karimnagar",
        "Tirupati",
        "Visakhapatnam",
        "Warangal",
        "Vijayawada"
    }

    actual_regions = {
        block["region"]
        for block in report
    }


    print("\n" + "=" * 65)
    print("TASK 3.1 ACCEPTANCE CHECK")
    print("=" * 65)

    print(
        "Unique flagged regions:",
        len(actual_regions)
    )

    print(
        "Expected unique flagged regions:",
        len(expected_regions)
    )


    if actual_regions == expected_regions:
        print("Unique region check: PASSED")
    else:
        print("Unique region check: FAILED")


    all_fields_present = all(
        block["Context"]
        and block["Insight"]
        and block["Implication"]
        for block in report
    )


    if all_fields_present:
        print("CII fields check: PASSED")
    else:
        print("CII fields check: FAILED")


    guntur_blocks = [
        block
        for block in report
        if block["region"] == "Guntur"
    ]


    if (
        len(guntur_blocks) == 1
        and
        len(guntur_blocks[0]["flagged_transitions"]) == 2
    ):

        print("Guntur combined-block check: PASSED")

    else:

        print("Guntur combined-block check: FAILED")


    if (
        actual_regions == expected_regions
        and
        all_fields_present
        and
        len(guntur_blocks) == 1
        and
        len(guntur_blocks[0]["flagged_transitions"]) == 2
    ):

        print("\nTASK 3.1: PASSED")

    else:

        print("\nTASK 3.1: CHECK REQUIRED")

    print("=" * 65)
