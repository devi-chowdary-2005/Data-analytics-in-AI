import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="PharmEasy Regional Pulse",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)


BASE_DIR = Path(__file__).resolve().parent

ORDERS_FILE = BASE_DIR / "orders_clean.csv"
REGIONS_FILE = BASE_DIR / "regions_master.csv"
REPORT_FILE = BASE_DIR / "draft_report_output.json"

MONTH_ORDER = ["Apr", "May", "Jun"]
THRESHOLD = 8.0


st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 0%,
            rgba(37, 99, 235, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(20, 184, 166, 0.08),
            transparent 25%
        ),
    color: #f8fafc;
}

.main .block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
        );
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] * {
    color: #f8fafc;
}

section[data-testid="stSidebar"] label {
    color: #cbd5e1 !important;
    font-weight: 700;
}


/* HERO */

.hero {
    background:
        linear-gradient(
            135deg,
        );

    border: 1px solid #263653;
    border-radius: 24px;

    padding: 36px 40px;
    margin-bottom: 22px;

    box-shadow:
        0 20px 55px rgba(0, 0, 0, 0.35);
}

.hero-badge {
    display: inline-block;

    padding: 7px 13px;

    border-radius: 999px;

    background: rgba(59, 130, 246, 0.12);
    border: 1px solid rgba(96, 165, 250, 0.25);

    color: #93c5fd;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 0.8px;
}

.hero-title {
    margin-top: 14px;

    color: #ffffff;

    font-size: 38px;
    font-weight: 850;

    letter-spacing: -1px;
}

.hero-subtitle {
    margin: 5px 0 0 0;

    color: #94a3b8;

    font-size: 15px;
}


/* SECTION */

.section-title {
    color: #f8fafc;

    font-size: 21px;
    font-weight: 800;

    margin-top: 26px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #64748b;

    font-size: 13px;

    margin-bottom: 12px;
}


/* KPI */

.kpi {
    background:
        linear-gradient(
            145deg,
        );

    border: 1px solid #1e293b;
    border-radius: 18px;

    padding: 19px;

    min-height: 125px;

    box-shadow:
        0 10px 28px rgba(0, 0, 0, 0.20);
}

.kpi-label {
    color: #64748b;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 0.8px;
    text-transform: uppercase;
}

.kpi-value {
    color: #f8fafc;

    font-size: 27px;
    font-weight: 850;

    margin-top: 8px;
}

.kpi-note {
    color: #64748b;

    font-size: 11px;

    margin-top: 4px;
}


/* MOVEMENT */

.movement {
    background: #0d1422;

    border: 1px solid #1e293b;

    border-radius: 16px;

    padding: 17px 19px;

    min-height: 120px;
}

.movement-label {
    color: #64748b;

    font-size: 11px;
    font-weight: 800;

    text-transform: uppercase;
}

.movement-value {
    color: #f8fafc;

    font-size: 26px;
    font-weight: 850;

    margin-top: 8px;
}

.movement-note {
    color: #64748b;

    font-size: 11px;

    margin-top: 3px;
}


/* INSIGHT */

.insight {
    background:
        linear-gradient(
            135deg,
            rgba(30, 64, 175, 0.20),
            rgba(13, 148, 136, 0.10)
        );

    border: 1px solid #1e40af;

    border-radius: 18px;

    padding: 20px 22px;

    margin-top: 10px;
}

.insight-title {
    color: #bfdbfe;

    font-size: 16px;
    font-weight: 800;

    margin-bottom: 7px;
}

.insight-text {
    color: #cbd5e1;

    font-size: 14px;
    line-height: 1.65;

    margin: 0;
}


/* WARNING */

.warning {
    background:
        linear-gradient(
            135deg,
            rgba(120, 53, 15, 0.25),
            rgba(67, 20, 7, 0.25)
        );

    border: 1px solid #92400e;

    border-radius: 18px;

    padding: 20px 22px;
}

.warning-title {
    color: #fdba74;

    font-size: 17px;
    font-weight: 800;

    margin-bottom: 8px;
}

.warning-text {
    color: #fed7aa;

    font-size: 14px;
    line-height: 1.65;
}


/* HIERARCHY */

.hierarchy {
    display: flex;

    align-items: center;

    gap: 8px;

    margin: 8px 0 20px 0;

    flex-wrap: wrap;
}

.hierarchy-item {
    background: #0f172a;

    border: 1px solid #263653;

    border-radius: 10px;

    padding: 8px 13px;

    color: #93c5fd;

    font-size: 11px;
    font-weight: 800;
}

.hierarchy-arrow {
    color: #475569;

    font-weight: 800;
}


/* DATAFRAME */

div[data-testid="stDataFrame"] {
    border: 1px solid #1e293b;
    border-radius: 14px;
}


/* EXPANDER */

div[data-testid="stExpander"] {
    background: #0d1422;

    border: 1px solid #1e293b;

    border-radius: 14px;
}


/* FOOTER */

.footer {
    text-align: center;

    color: #475569;

    font-size: 11px;

    padding-top: 30px;
}

</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_orders():

    df = pd.read_csv(ORDERS_FILE)

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    df["sales_inr"] = pd.to_numeric(
        df["sales_inr"],
        errors="coerce"
    )

    df["profit_inr"] = pd.to_numeric(
        df["profit_inr"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["month"] = df["order_date"].dt.strftime("%b")

    df["month"] = pd.Categorical(
        df["month"],
        categories=MONTH_ORDER,
        ordered=True
    )

    return df


@st.cache_data
def load_regions():

    return pd.read_csv(REGIONS_FILE)


@st.cache_data
def load_report():

    if not REPORT_FILE.exists():
        return []

    try:

        with open(
            REPORT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return []


orders = load_orders()
regions = load_regions()
report_data = load_report()


required_columns = [
    "order_id",
    "order_date",
    "region",
    "category",
    "product",
    "quantity",
    "sales_inr",
    "profit_inr",
]

missing_columns = [
    column
    for column in required_columns
    if column not in orders.columns
]

if missing_columns:

    st.error(
        "Missing columns in orders_clean.csv: "
        + ", ".join(missing_columns)
    )

    st.stop()


def rupees(value):

    if pd.isna(value):

        return "₹0"

    return f"₹{float(value):,.0f}"


def safe_mom(current, previous):
    if pd.isna(previous):
        return np.nan

    if previous == 0:
        return np.nan

    if pd.isna(current):
        return np.nan

    return (
        (current - previous)
        / previous
        * 100
    )


def calculate_metrics(df):

    total_sales = df["sales_inr"].sum()

    total_profit = df["profit_inr"].sum()

    total_orders = df["order_id"].nunique()

    active_regions = df["region"].nunique()

    monthly = (
        df.groupby(
            "month",
            observed=False
        )
        .agg(
            sales=("sales_inr", "sum"),
            profit=("profit_inr", "sum"),
            orders=("order_id", "nunique")
        )
        .reset_index()
    )

    monthly["month"] = pd.Categorical(
        monthly["month"],
        categories=MONTH_ORDER,
        ordered=True
    )

    monthly = monthly.sort_values(
        "month"
    )

    monthly["mom"] = (
        monthly["sales"]
        .pct_change(fill_method=None)
        * 100
    )

    return (
        total_sales,
        total_profit,
        total_orders,
        active_regions,
        monthly
    )


def get_flagged_regions(df):
    monthly = (
        df.groupby(
            ["region", "month"],
            observed=False
        )["sales_inr"]
        .sum()
        .reset_index()
    )

    all_regions = regions["region"].dropna().unique().tolist()

    region_index = pd.MultiIndex.from_product(
        [all_regions, MONTH_ORDER],
        names=["region", "month"]
    )

    monthly = (
        monthly.set_index(["region", "month"])
        .reindex(region_index, fill_value=0)
        .reset_index()
    )

    pivot = monthly.pivot(
        index="region",
        columns="month",
        values="sales_inr"
    )

    pivot = pivot.reindex(
        index=all_regions,
        columns=MONTH_ORDER,
        fill_value=0
    )

    pivot["Apr"] = pd.to_numeric(pivot["Apr"], errors="coerce")
    pivot["May"] = pd.to_numeric(pivot["May"], errors="coerce")
    pivot["Jun"] = pd.to_numeric(pivot["Jun"], errors="coerce")

    pivot["Apr_May"] = np.where(
        pivot["Apr"] != 0,
        (pivot["May"] - pivot["Apr"]) / pivot["Apr"] * 100,
        np.nan
    )

    pivot["May_Jun"] = np.where(
        pivot["May"] != 0,
        (pivot["Jun"] - pivot["May"]) / pivot["May"] * 100,
        np.nan
    )

    pivot["Apr_May"] = pd.to_numeric(
        pivot["Apr_May"],
        errors="coerce"
    )

    pivot["May_Jun"] = pd.to_numeric(
        pivot["May_Jun"],
        errors="coerce"
    )

    pivot["flagged"] = (
        pivot["Apr_May"].abs().gt(THRESHOLD)
        |
        pivot["May_Jun"].abs().gt(THRESHOLD)
    )

    return pivot.reset_index()


with st.sidebar:

    st.html(
        """
        <div style="
            text-align:center;
            padding:15px 0 25px 0;
        ">

            <div style="
                font-size:42px;
            ">
                💊
            </div>

            <div style="
                color:white;
                font-size:21px;
                font-weight:800;
            ">
                PharmEasy
            </div>

            <div style="
                color:#64748b;
                font-size:12px;
                margin-top:3px;
            ">
                Regional Pulse
            </div>

        </div>
        """
    )

    st.markdown("### Dashboard Controls")

    region_options = [
        "All Regions"
    ] + sorted(
        regions["region"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_region = st.selectbox(
        "Region",
        region_options
    )

    category_options = [
        "All Categories"
    ] + sorted(
        orders["category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Category",
        category_options
    )

    st.markdown("---")

    st.markdown(
        """
        **REPORTING PERIOD**

        April – June 2026

        **ALERT THRESHOLD**

        Absolute MoM change > 8%

        **DATA COVERAGE**

        2,100 cleaned orders  
        10 master regions
        """
    )


filtered = orders.copy()

if selected_region != "All Regions":

    filtered = filtered[
        filtered["region"]
        == selected_region
    ]

if selected_category != "All Categories":

    filtered = filtered[
        filtered["category"]
        == selected_category
    ]


st.html(
    """
    <div class="hero">

        <div class="hero-badge">
            REGIONAL BUSINESS INTELLIGENCE
            • APR–JUN 2026
        </div>

        <div class="hero-title">
            PharmEasy Regional Pulse
        </div>

        <p class="hero-subtitle">
            Regional sales movement,
            operational alerts and
            decision-ready insights.
        </p>

    </div>
    """
)


st.html(
    """
    <div class="hierarchy">

        <div class="hierarchy-item">
            LEVEL 1 · EXECUTIVE PULSE
        </div>

        <div class="hierarchy-arrow">
            →
        </div>

        <div class="hierarchy-item">
            LEVEL 2 · REGIONAL PERFORMANCE
        </div>

        <div class="hierarchy-arrow">
            →
        </div>

        <div class="hierarchy-item">
            LEVEL 3 · CATEGORY DETAIL
        </div>

    </div>
    """
)


(
    total_sales,
    total_profit,
    total_orders,
    active_regions,
    monthly
) = calculate_metrics(filtered)


avg_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    total_profit
    / total_sales
    * 100
    if total_sales > 0
    else 0
)


st.markdown(
    '<div class="section-title">'
    'Executive Pulse'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'High-level view of the selected reporting scope.'
    '</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)


def create_kpi(
    column,
    label,
    value,
    note
):

    column.html(
        f"""
        <div class="kpi">

            <div class="kpi-label">
                {label}
            </div>

            <div class="kpi-value">
                {value}
            </div>

            <div class="kpi-note">
                {note}
            </div>

        </div>
        """
    )


create_kpi(
    k1,
    "Total Sales",
    rupees(total_sales),
    "April–June"
)

create_kpi(
    k2,
    "Total Profit",
    rupees(total_profit),
    f"{profit_margin:.1f}% margin"
)

create_kpi(
    k3,
    "Orders",
    f"{total_orders:,}",
    "Unique orders"
)

create_kpi(
    k4,
    "Active Regions",
    str(active_regions),
    "Regions with orders"
)

create_kpi(
    k5,
    "Avg Order Value",
    rupees(avg_order_value),
    "Sales ÷ orders"
)


st.markdown(
    '<div class="section-title">'
    'Month-on-Month Movement'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Both reporting transitions are shown explicitly.'
    '</div>',
    unsafe_allow_html=True
)


def get_month_sales(
    monthly_df,
    month
):

    result = monthly_df.loc[
        monthly_df["month"] == month,
        "sales"
    ]

    if result.empty:
        return 0.0

    value = result.iloc[0]

    if pd.isna(value):
        return 0.0

    return float(value)


apr_sales = get_month_sales(
    monthly,
    "Apr"
)

may_sales = get_month_sales(
    monthly,
    "May"
)

jun_sales = get_month_sales(
    monthly,
    "Jun"
)


apr_may = safe_mom(
    may_sales,
    apr_sales
)

may_jun = safe_mom(
    jun_sales,
    may_sales
)


m1, m2 = st.columns(2)


with m1:

    apr_may_display = (
        f"{apr_may:+.2f}%"
        if not pd.isna(apr_may)
        else "N/A"
    )

    st.html(
        f"""
        <div class="movement">

            <div class="movement-label">
                April → May
            </div>

            <div class="movement-value">
                {apr_may_display}
            </div>

            <div class="movement-note">
                {rupees(apr_sales)}
                →
                {rupees(may_sales)}
            </div>

        </div>
        """
    )


with m2:

    may_jun_display = (
        f"{may_jun:+.2f}%"
        if not pd.isna(may_jun)
        else "N/A"
    )

    st.html(
        f"""
        <div class="movement">

            <div class="movement-label">
                May → June
            </div>

            <div class="movement-value">
                {may_jun_display}
            </div>

            <div class="movement-note">
                {rupees(may_sales)}
                →
                {rupees(jun_sales)}
            </div>

        </div>
        """
    )


st.markdown(
    '<div class="section-title">'
    'Executive Summary'
    '</div>',
    unsafe_allow_html=True
)


if selected_region == "All Regions":

    apr_display = (
        f"{apr_may:+.2f}%"
        if not pd.isna(apr_may)
        else "N/A"
    )

    jun_display = (
        f"{may_jun:+.2f}%"
        if not pd.isna(may_jun)
        else "N/A"
    )

    summary = (
        "Across April–June 2026, the cleaned dataset contains "
        "2,100 orders across nine active order regions. "
        f"Network sales changed {apr_display} from April to May "
        f"and {jun_display} from May to June. "
        "Regional movements are monitored against the fixed "
        "8% operational-alert threshold. "
        "The dataset establishes sales movements but does not "
        "establish their underlying causes."
    )

else:

    summary = (
        f"{selected_region} generated "
        f"{rupees(total_sales)} in sales. "
        f"Sales changed "
        f"{apr_may:+.2f}% from April to May "
        f"and "
        f"{may_jun:+.2f}% from May to June. "
        "These movements are evaluated against the fixed "
        "8% operational-alert threshold. "
        "The dataset establishes the direction and size "
        "of the movement but not its underlying cause."
    )


st.html(
    f"""
    <div class="insight">

        <div class="insight-title">
            📌 Decision Context
        </div>

        <p class="insight-text">
            {summary}
        </p>

    </div>
    """
)


st.markdown(
    '<div class="section-title">'
    'Sales Trend'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'April, May and June sales movement.'
    '</div>',
    unsafe_allow_html=True
)


fig_trend = go.Figure()

fig_trend.add_trace(
    go.Scatter(
        x=monthly["month"],
        y=monthly["sales"],
        mode="lines+markers",

        line=dict(
            color="#60a5fa",
            width=4
        ),

        marker=dict(
            color="#38bdf8",
            size=11
        ),

        fill="tozeroy",

        fillcolor="rgba(56,189,248,0.08)",

        hovertemplate=(
            "%{x}"
            "<br>Sales: ₹%{y:,.0f}"
            "<extra></extra>"
        )
    )
)

fig_trend.update_layout(
    height=370,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    paper_bgcolor="#0d1422",
    plot_bgcolor="#0d1422",

    font=dict(
        color="#cbd5e1"
    ),

    xaxis=dict(
        title=None,
        gridcolor="#1e293b"
    ),

    yaxis=dict(
        title="Sales (₹)",
        gridcolor="#1e293b"
    ),

    hovermode="x unified"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


st.markdown(
    '<div class="section-title">'
    'Regional Performance'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Regional contribution and category mix.'
    '</div>',
    unsafe_allow_html=True
)


regional_sales = (
    regions[["region"]]
    .drop_duplicates()
    .merge(
        filtered.groupby(
            "region",
            as_index=False
        )["sales_inr"].sum(),
        on="region",
        how="left"
    )
    .fillna({"sales_inr": 0})
    .sort_values(
        "sales_inr",
        ascending=False
    )
)

regional_sales = regional_sales.rename(
    columns={
        "sales_inr": "sales"
    }
)


left, right = st.columns(
    [1.25, 1]
)


with left:

    fig_bar = px.bar(
        regional_sales,
        x="sales",
        y="region",
        orientation="h",
        text="sales"
    )

    fig_bar.update_traces(
        marker_color="#3b82f6",
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig_bar.update_layout(
        height=450,

        margin=dict(
            l=10,
            r=90,
            t=20,
            b=20
        ),

        paper_bgcolor="#0d1422",
        plot_bgcolor="#0d1422",

        font=dict(
            color="#cbd5e1"
        ),

        xaxis=dict(
            title="Sales (₹)",
            gridcolor="#1e293b"
        ),

        yaxis=dict(
            title=None,
            gridcolor="#0d1422"
        ),

        showlegend=False
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )


with right:

    category_sales = (
        filtered
        .groupby(
            "category",
            as_index=False
        )["sales_inr"]
        .sum()
        .sort_values(
            "sales_inr",
            ascending=False
        )
    )

    if category_sales.empty:
        st.info("No order data is available for the selected scope.")
    else:
        fig_donut = px.pie(
            category_sales,
            names="category",
            values="sales_inr",
            hole=0.60
        )

        fig_donut.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "%{label}"
                "<br>₹%{value:,.0f}"
                "<extra></extra>"
            )
        )

        fig_donut.update_layout(
            height=450,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=20
            ),
            paper_bgcolor="#0d1422",
            plot_bgcolor="#0d1422",
            font=dict(
                color="#cbd5e1"
            ),
            legend=dict(
                orientation="h",
                y=-0.08
            )
        )

        st.plotly_chart(
            fig_donut,
            use_container_width=True
        )


st.markdown(
    '<div class="section-title">'
    'Regional Movement Alerts'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Flagged when absolute Month-on-Month movement is greater than 8%.'
    '</div>',
    unsafe_allow_html=True
)


flagged = get_flagged_regions(
    filtered
)


flagged_display = flagged[
    [
        "region",
        "Apr_May",
        "May_Jun",
        "flagged"
    ]
].copy()


flagged_display = flagged_display.rename(
    columns={
        "region": "Region",
        "Apr_May": "Apr → May %",
        "May_Jun": "May → Jun %",
        "flagged": "Alert"
    }
)


flagged_display[
    "Apr → May %"
] = pd.to_numeric(
    flagged_display[
        "Apr → May %"
    ],
    errors="coerce"
).round(2)


flagged_display[
    "May → Jun %"
] = pd.to_numeric(
    flagged_display[
        "May → Jun %"
    ],
    errors="coerce"
).round(2)


st.dataframe(
    flagged_display,
    use_container_width=True,
    hide_index=True,

    column_config={

        "Apr → May %":
            st.column_config.NumberColumn(
                format="%.2f%%"
            ),

        "May → Jun %":
            st.column_config.NumberColumn(
                format="%.2f%%"
            ),

        "Alert":
            st.column_config.CheckboxColumn(
                "Alert"
            )
    }
)


st.markdown(
    '<div class="section-title">'
    'Key CII Finding'
    '</div>',
    unsafe_allow_html=True
)


if selected_region in [
    "All Regions",
    "Guntur"
]:

    st.html(
        """
        <div class="warning">

            <div class="warning-title">
                ⚠️ Guntur requires human review
            </div>

            <div class="warning-text">

                Guntur sales increased from
                <b>₹62,442.27</b> in April 2026
                to <b>₹138,738.93</b> in May 2026,
                a <b>+122.19%</b> Month-on-Month movement.

                <br><br>

                Sales then declined to
                <b>₹99,745.18</b> in June,
                representing a
                <b>-28.11%</b> Month-on-Month movement.

                <br><br>

                The dataset establishes the movement,
                but does not establish the underlying cause.
                Human review should examine order-level
                and category-level patterns before
                operational action.

            </div>

        </div>
        """
    )

else:

    st.success(
        f"Regional drill-down active for {selected_region}."
    )


st.markdown(
    '<div class="section-title">'
    'Category Detail'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Level 3 category drill-down.'
    '</div>',
    unsafe_allow_html=True
)


category_monthly = (
    filtered
    .groupby(
        ["category", "month"],
        observed=False
    )["sales_inr"]
    .sum()
    .reset_index()
)


category_monthly["month"] = pd.Categorical(
    category_monthly["month"],
    categories=MONTH_ORDER,
    ordered=True
)


category_monthly = category_monthly.sort_values(
    ["category", "month"]
)


fig_category = px.line(
    category_monthly,
    x="month",
    y="sales_inr",
    color="category",
    markers=True
)


fig_category.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)


fig_category.update_layout(
    height=430,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    paper_bgcolor="#0d1422",
    plot_bgcolor="#0d1422",

    font=dict(
        color="#cbd5e1"
    ),

    xaxis=dict(
        title=None,
        gridcolor="#1e293b"
    ),

    yaxis=dict(
        title="Sales (₹)",
        gridcolor="#1e293b"
    ),

    legend_title=None
)


st.plotly_chart(
    fig_category,
    use_container_width=True
)


st.markdown(
    '<div class="section-title">'
    'Top Products'
    '</div>',
    unsafe_allow_html=True
)


product_sales = (
    filtered
    .groupby(
        "product",
        as_index=False
    )
    .agg(
        sales=(
            "sales_inr",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        )
    )
    .sort_values(
        "sales",
        ascending=False
    )
    .head(10)
)


st.dataframe(
    product_sales,
    use_container_width=True,
    hide_index=True,

    column_config={

        "sales":
            st.column_config.NumberColumn(
                "Sales (₹)",
                format="₹%,.2f"
            ),

        "orders":
            st.column_config.NumberColumn(
                "Orders"
            )
    }
)


with st.expander(
    "ℹ️ Methodology & Reliability"
):

    st.markdown(
        """

The dashboard uses the cleaned PharmEasy regional dataset.

Duplicate rows were removed, region names were normalized,
missing category values were imputed using product-category
mapping, and missing profit values were imputed using
category-level mean profit margins.


April → May:

**(May Sales − April Sales) / April Sales × 100**

May → June:

**(June Sales − May Sales) / May Sales × 100**

A region is flagged when:

**absolute MoM change > 8%**


A region with zero sales in the previous month is not assigned
an artificial percentage change. Its MoM value is displayed
as N/A because percentage change from a zero base is undefined.


The dashboard identifies sales movements.

It does not independently establish why those movements
occurred.

External explanations must therefore be treated as
hypotheses until validated by additional evidence.


Recommendations pass through the human review gate
and are recorded in `audit_log.jsonl`.
"""
    )


st.html(
    """
    <div class="footer">
        PharmEasy Regional Pulse
        · Decision Intelligence Dashboard
        · 2026
    </div>
    """
)
