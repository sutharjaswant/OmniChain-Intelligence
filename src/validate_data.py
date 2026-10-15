
from pathlib import Path
import pandas as pd

# Find the folder containing our CSV files
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

if not (DATA_DIR / "orders.csv").exists():
    DATA_DIR = DATA_DIR / "raw"

required_files = [
    "orders.csv",
    "products.csv",
    "customers.csv",
    "inventory.csv",
    "suppliers.csv",
    "supplier_deliveries.csv",
]

print("\nOMNCHAIN INTELLIGENCE - DATA VALIDATION")
print("=" * 45)

missing_files = [
    filename for filename in required_files
    if not (DATA_DIR / filename).exists()
]

if missing_files:
    print("Missing files:", missing_files)
    raise SystemExit("Please check the data folder and file names.")

data = {}

for filename in required_files:
    df = pd.read_csv(DATA_DIR / filename)
    data[filename] = df

    print(f"\n{filename}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Missing values: {df.isna().sum().sum()}")

# Check primary-key uniqueness
key_checks = {
    "products.csv": "ProductID",
    "customers.csv": "CustomerID",
    "suppliers.csv": "SupplierID",
}

print("\nPRIMARY KEY CHECKS")
print("=" * 45)

for filename, key in key_checks.items():
    df = data[filename]
    duplicate_keys = df[key].duplicated().sum()
    print(f"{filename} - duplicate {key}: {duplicate_keys}")

# Check order references
orders = data["orders.csv"]
products = data["products.csv"]
customers = data["customers.csv"]

unknown_products = (~orders["ProductID"].isin(products["ProductID"])).sum()
unknown_customers = (~orders["CustomerID"].isin(customers["CustomerID"])).sum()

print("\nRELATIONSHIP CHECKS")
print("=" * 45)
print("Orders with unknown products:", unknown_products)
print("Orders with unknown customers:", unknown_customers)

# Check financial calculations
cancelled = orders["Status"].eq("Cancelled")
active_orders = orders.loc[~cancelled]

expected_revenue = (
    active_orders["GrossSales"] - active_orders["DiscountAmount"]
)
revenue_errors = (
    expected_revenue - active_orders["NetRevenue"]
).abs().gt(0.01).sum()

expected_profit = (
    active_orders["NetRevenue"]
    - active_orders["ProductCost"]
    - active_orders["ShippingCost"]
)
profit_errors = (
    expected_profit - active_orders["GrossProfit"]
).abs().gt(0.01).sum()

print("\nFINANCIAL CHECKS")
print("=" * 45)
print("Revenue calculation errors:", revenue_errors)
print("Profit calculation errors:", profit_errors)

print("\nVALIDATION SCRIPT COMPLETED")
print("Review every result before using the data in Power BI.")
