"""Task 2: Exploratory Data Analysis (EDA) with Pandas, Matplotlib and Seaborn.

Run from the project folder:
    python -m pip install -r requirements.txt
    python task2_eda.py

Input: cleaned_sales_data.csv (the cleaned output from Task 1)
Outputs: eda_charts/*.png, eda_summary.txt, product_summary.csv,
         region_summary.csv, category_summary.csv, payment_summary.csv,
         daily_sales_summary.csv
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "cleaned_sales_data.csv"
CHART_DIR = BASE_DIR / "eda_charts"
CHART_DIR.mkdir(exist_ok=True)

REQUIRED_COLUMNS = {
    "Order_ID", "Order_Date", "Product", "Category", "Quantity",
    "Unit_Price", "Region", "Payment_Method", "Customer_Age", "Sales_Amount"
}


def load_data() -> pd.DataFrame:
    """Load and validate the cleaned sales dataset."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_FILE.name}. Keep it in the same folder as task2_eda.py."
        )
    df = pd.read_csv(INPUT_FILE)
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for col in ["Quantity", "Unit_Price", "Customer_Age", "Sales_Amount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Order_Date", "Sales_Amount", "Quantity", "Unit_Price"]).copy()
    return df


def create_charts(df: pd.DataFrame) -> None:
    """Create the core visualizations requested for the EDA task."""
    sns.set_theme(style="whitegrid", context="notebook")

    # 1. Distribution of sales per order
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=df, x="Sales_Amount", bins=8, kde=True, ax=ax, color="#167D9A")
    ax.axvline(df["Sales_Amount"].mean(), color="#C44E52", linestyle="--", label=f"Mean = ₹{df['Sales_Amount'].mean():,.0f}")
    ax.axvline(df["Sales_Amount"].median(), color="#4C72B0", linestyle=":", label=f"Median = ₹{df['Sales_Amount'].median():,.0f}")
    ax.set(title="Distribution of Sales Amount per Order", xlabel="Sales amount (₹)", ylabel="Number of orders")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "01_sales_amount_distribution.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # 2. Order counts by product
    product_orders = df["Product"].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    product_orders.plot(kind="barh", ax=ax, color="#4C9F70")
    ax.set(title="Number of Orders by Product", xlabel="Number of orders", ylabel="Product")
    for i, val in enumerate(product_orders.values):
        ax.text(val + 0.08, i, str(val), va="center", fontsize=9)
    ax.set_xlim(0, max(product_orders.values) + 1.5)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "02_orders_by_product.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # 3. Total revenue by product
    product_sales = df.groupby("Product")["Sales_Amount"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    product_sales.plot(kind="barh", ax=ax, color="#D18F36")
    ax.set(title="Total Sales by Product", xlabel="Total sales (₹)", ylabel="Product")
    for i, val in enumerate(product_sales.values):
        ax.text(val + 45, i, f"₹{val:,.0f}", va="center", fontsize=9)
    ax.set_xlim(0, max(product_sales.values) * 1.18)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "03_revenue_by_product.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # 4. Total sales by region
    region_sales = df.groupby("Region")["Sales_Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=region_sales.values, y=region_sales.index, ax=ax, color="#8172B2")
    ax.set(title="Total Sales by Region", xlabel="Total sales (₹)", ylabel="Region")
    for i, val in enumerate(region_sales.values):
        ax.text(val + 35, i, f"₹{val:,.0f}", va="center", fontsize=9)
    ax.set_xlim(0, max(region_sales.values) * 1.18)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "04_sales_by_region.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # 5. Daily sales trend
    daily_sales = df.groupby("Order_Date", as_index=False)["Sales_Amount"].sum().sort_values("Order_Date")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=daily_sales, x="Order_Date", y="Sales_Amount", marker="o", ax=ax, color="#167D9A")
    ax.set(title="Daily Sales Trend", xlabel="Order date", ylabel="Total sales per day (₹)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "05_daily_sales_trend.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # 6. Unit price vs sales amount
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x="Unit_Price", y="Sales_Amount", hue="Category", s=90, ax=ax, palette="Set2")
    ax.set(title="Unit Price vs. Sales Amount", xlabel="Unit price (₹)", ylabel="Sales amount per order (₹)")
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "06_unit_price_vs_sales.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # 7. Category sales share
    category_sales = df.groupby("Category")["Sales_Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7.5, 5))
    category_sales.plot(kind="bar", ax=ax, color=["#4C9F70", "#D18F36", "#8172B2"])
    ax.set(title="Total Sales by Category", xlabel="Category", ylabel="Total sales (₹)")
    ax.tick_params(axis="x", rotation=15)
    for i, val in enumerate(category_sales.values):
        ax.text(i, val + 100, f"₹{val:,.0f}", ha="center", fontsize=9)
    ax.set_ylim(0, max(category_sales.values) * 1.18)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "07_sales_by_category.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def create_summaries(df: pd.DataFrame) -> str:
    """Save analysis tables and a concise written interpretation."""
    product_summary = df.groupby("Product").agg(
        Orders=("Order_ID", "count"), Units_Sold=("Quantity", "sum"),
        Total_Sales=("Sales_Amount", "sum"), Average_Order_Sales=("Sales_Amount", "mean")
    ).sort_values("Total_Sales", ascending=False).round(2)
    category_summary = df.groupby("Category").agg(
        Orders=("Order_ID", "count"), Units_Sold=("Quantity", "sum"), Total_Sales=("Sales_Amount", "sum")
    ).sort_values("Total_Sales", ascending=False).round(2)
    region_summary = df.groupby("Region").agg(
        Orders=("Order_ID", "count"), Total_Sales=("Sales_Amount", "sum"),
        Average_Order_Sales=("Sales_Amount", "mean")
    ).sort_values("Total_Sales", ascending=False).round(2)
    payment_summary = df.groupby("Payment_Method").agg(
        Orders=("Order_ID", "count"), Total_Sales=("Sales_Amount", "sum")
    ).sort_values("Orders", ascending=False).round(2)
    daily_summary = df.groupby("Order_Date", as_index=False).agg(
        Orders=("Order_ID", "count"), Total_Sales=("Sales_Amount", "sum")
    ).sort_values("Order_Date")

    product_summary.to_csv(BASE_DIR / "product_summary.csv")
    category_summary.to_csv(BASE_DIR / "category_summary.csv")
    region_summary.to_csv(BASE_DIR / "region_summary.csv")
    payment_summary.to_csv(BASE_DIR / "payment_summary.csv")
    daily_summary.to_csv(BASE_DIR / "daily_sales_summary.csv", index=False, date_format="%Y-%m-%d")

    total_sales = float(df["Sales_Amount"].sum())
    mean_sales = float(df["Sales_Amount"].mean())
    median_sales = float(df["Sales_Amount"].median())
    top_product = product_summary.index[0]
    top_product_sales = int(product_summary.iloc[0]["Total_Sales"])
    top_region_orders = df["Region"].value_counts().idxmax()
    top_region_order_count = int(df["Region"].value_counts().max())
    top_region_revenue = region_summary.index[0]
    top_region_revenue_value = int(region_summary.iloc[0]["Total_Sales"])
    top_category = category_summary.index[0]
    top_category_sales = int(category_summary.iloc[0]["Total_Sales"])
    top_payment = df["Payment_Method"].value_counts().idxmax()
    top_payment_count = int(df["Payment_Method"].value_counts().max())
    highest_day = daily_summary.loc[daily_summary["Total_Sales"].idxmax()]
    highest_day_date = pd.to_datetime(highest_day["Order_Date"]).strftime("%d %b %Y")
    highest_day_sales = int(highest_day["Total_Sales"])
    corr_price = float(df["Unit_Price"].corr(df["Sales_Amount"]))
    corr_qty = float(df["Quantity"].corr(df["Sales_Amount"]))
    missing_values = int(df.isna().sum().sum())

    q1 = float(df["Sales_Amount"].quantile(0.25))
    q3 = float(df["Sales_Amount"].quantile(0.75))
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    possible_outliers = df.loc[df["Sales_Amount"] > upper_bound, ["Order_ID", "Product", "Sales_Amount"]]

    summary = f"""TASK 2: EXPLORATORY DATA ANALYSIS (EDA) — RESULTS
Dataset: Cleaned fictional sales dataset from Task 1
Rows analysed: {len(df)}
Date range: {df['Order_Date'].min():%d %b %Y} to {df['Order_Date'].max():%d %b %Y}
Missing values in analysis data: {missing_values}

OVERALL SALES
Total sales: ₹{total_sales:,.2f}
Mean sales per order: ₹{mean_sales:,.2f}
Median sales per order: ₹{median_sales:,.2f}
Mean vs median: mean > median, consistent with a right-skewed distribution caused by a small number of higher-value orders.

PRODUCT INSIGHTS
Top product by total sales: {top_product} (₹{top_product_sales:,.0f})
{product_summary.to_string()}

CATEGORY INSIGHTS
Top category by total sales: {top_category} (₹{top_category_sales:,.0f})
{category_summary.to_string()}

REGION INSIGHTS
Region with most orders: {top_region_orders} ({top_region_order_count} orders)
Region with highest total sales: {top_region_revenue} (₹{top_region_revenue_value:,.0f})
{region_summary.to_string()}

PAYMENT METHOD INSIGHTS
Most frequently used payment method: {top_payment} ({top_payment_count} of {len(df)} orders)
{payment_summary.to_string()}

TIME-BASED INSIGHT
Highest-sales day: {highest_day_date} (₹{highest_day_sales:,.0f})

RELATIONSHIPS AND POSSIBLE OUTLIERS
Correlation between Unit_Price and Sales_Amount: {corr_price:.3f}
Correlation between Quantity and Sales_Amount: {corr_qty:.3f}
The positive unit-price relationship is expected because order sales are calculated as quantity multiplied by unit price. The negative quantity correlation should not be interpreted as quantity reducing sales; products with larger unit prices tend to have smaller quantities in this small sample.
IQR upper threshold for Sales_Amount: ₹{upper_bound:,.2f}
Potential high-value points above that threshold: {len(possible_outliers)}. Review them in context; a statistical outlier is not automatically an error.
{possible_outliers.to_string(index=False) if len(possible_outliers) else 'No sales-amount points above the IQR threshold.'}

SUMMARY OF FINDINGS
1. {top_product} generated the largest total sales (₹{top_product_sales:,.0f}) even though it did not have the highest order count.
2. {top_category} led sales by category (₹{top_category_sales:,.0f}); stationery generated more order volume but lower total sales.
3. {top_region_orders} recorded the most orders ({top_region_order_count}), while {top_region_revenue} generated the largest total sales.
4. {top_payment} was the most frequently selected payment method.
5. Daily sales varied; {highest_day_date} was the strongest day in this sample.
6. The dataset is small and fictional, so findings illustrate EDA techniques rather than representing a real business. Validate any decisions with larger real-world data.
"""
    (BASE_DIR / "eda_summary.txt").write_text(summary, encoding="utf-8")
    return summary


def main() -> None:
    df = load_data()
    create_charts(df)
    summary = create_summaries(df)
    print("EDA completed successfully.")
    print(f"Rows analysed: {len(df)}")
    print(f"Total sales: ₹{df['Sales_Amount'].sum():,.2f}")
    print(f"Charts saved to: {CHART_DIR}")
    print(f"Summary saved to: {BASE_DIR / 'eda_summary.txt'}")
    print("\n" + summary)


if __name__ == "__main__":
    main()
