# OmniChain Intelligence — Retail Supply Chain Analytics

An end-to-end data analytics project that analyzes retail sales, customer behavior, inventory levels, and supplier performance using Python, SQL, and Power BI.

## Project Overview

OmniChain Intelligence is a retail analytics project designed to turn raw business data into meaningful insights. It helps analyze sales performance, monitor inventory, identify products requiring restocking, and evaluate supplier delivery performance through an interactive Power BI dashboard.

**Note:** This project uses synthetic data generated for learning and portfolio demonstration purposes.

## Business Objectives

- Analyze revenue and profit performance.
- Track monthly sales trends and product category performance.
- Identify products that need restocking.
- Evaluate supplier on-time delivery and lead times.
- Build an interactive dashboard to support data-driven decisions.

## Technologies Used

- **Python:** Data generation, processing, and quality checks
- **Pandas & NumPy:** Data manipulation and analysis
- **SQLite:** Database storage and SQL analysis
- **SQL:** Business queries and performance analysis
- **Power BI:** Interactive dashboards and visualizations
- **Git & GitHub:** Version control and project hosting

## Dashboard Pages

### 1. Executive Overview
- Revenue and profit KPIs
- Monthly revenue trends
- Revenue by product category
- Top 10 products by revenue
- Order status breakdown

### 2. Supplier Performance Analysis
- Total supplier deliveries
- On-time delivery percentage
- Average supplier lead time
- Supplier performance comparisons
- Supplier summary table

### 3. Inventory & Product Insights
- Total number of products
- Products requiring restocking
- Total inventory units
- Stock-level analysis
- Product inventory details

## Key Project Metrics

| Metric | Result |
|---|---:|
| Order records | 1,800 |
| Customers | 180 |
| Products | 60 |
| Suppliers | 12 |
| Supplier delivery records | 480 |
| Net revenue | ₹15,67,945.56 |
| Gross profit | ₹5,74,897.34 |
| Products requiring restocking | 14 |

*These figures are based on the generated synthetic dataset.*

## Data Quality

The project includes automated database checks to validate key fields, unique identifiers, table relationships, revenue and profit calculations, and inventory conditions.

**Latest recorded result:** 17 checks passed and 0 failed.

## Project Structure

```text
OmniChain-Intelligence/
├── data/
│   ├── raw/
│   └── processed/
├── dashboard/
│   └── OmniChain_Intelligence.pbix
├── docs/
├── sql/
│   └── 01_business_analysis.sql
├── src/
│   ├── data.py
│   ├── load_database.py
│   ├── test_database.py
│   ├── quality_checks.py
│   └── run_sql.py
└── README.md
```

## Key Business Insights

- The Outdoor category generated the highest revenue among the analyzed categories.
- November recorded the highest monthly revenue in the generated dataset.
- Fourteen products met the project's restocking condition.
- Supplier delivery performance varies, making supplier-level comparisons useful for identifying improvement opportunities.

## How to Run the Project

1. Clone or download this repository.
2. Install Python 3.11 or a compatible version.
3. Create and activate a virtual environment.
4. Install the required packages.
5. Run the data-generation script.
6. Run the database-loading script.
7. Execute the quality checks and SQL analysis.
8. Open the Power BI `.pbix` file to explore the dashboards.

## Future Improvements

- Add sales forecasting.
- Build automated inventory alerts.
- Develop supplier risk scoring.
- Add a natural-language analytics interface.
- Connect the dashboard to regularly updated data.

## Disclaimer

OmniChain Intelligence is an educational portfolio project. All business data is synthetic and does not represent an actual company.

---

**Built with Python, SQL, SQLite, and Power BI.**