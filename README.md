# Task 2 — Exploratory Data Analysis (EDA)

**CodeOrbit Tech — Data Science Internship**

This project explores the cleaned fictional sales dataset created in Task 1 using Python, Pandas, Matplotlib, and Seaborn.

## Project contents

- `task2_eda.ipynb` — step-by-step Jupyter/Google Colab notebook
- `task2_eda.py` — runnable Python script
- `cleaned_sales_data.csv` — cleaned practice dataset from Task 1
- `Task2_EDA_Submission_Report.docx` — editable report (replace `[Enter your name]` before submitting)
- `Task2_EDA_Submission_Report.pdf` — PDF report
- `eda_summary.txt` — written findings and interpretations
- `eda_charts/` — generated charts
- `product_summary.csv`, `category_summary.csv`, `region_summary.csv`, `payment_summary.csv`, `daily_sales_summary.csv` — analysis tables

## Run locally

1. Install Python 3.10 or newer.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Keep `cleaned_sales_data.csv` in the same folder as `task2_eda.py`.
4. Run:
   ```bash
   python task2_eda.py
   ```

The script generates the charts and summary tables in this folder.

## Run in Google Colab

1. Upload `task2_eda.ipynb` to Google Colab.
2. Upload `cleaned_sales_data.csv` through Colab's left Files panel.
3. Ensure the filename is exactly `cleaned_sales_data.csv`.
4. Select **Runtime → Run all**.

## Main findings (practice dataset)

- 30 cleaned orders were analyzed.
- Total sales were ₹15,538.
- Mean order sales were ₹517.93; median order sales were ₹385.00.
- Backpack led total sales by product (₹6,293).
- Accessories led category sales (₹9,543).
- Chennai had the highest regional total sales (₹4,917).
- UPI was the most common payment method (15 of 30 orders).
- 8 January 2026 had the highest daily sales total (₹2,548).

## Important limitation

The dataset is fictional and small, and is intended for practice. These findings demonstrate EDA methods and should not be treated as real business conclusions. Review the report and replace the author-name placeholder before submitting.
