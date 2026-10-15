
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "omnichain.db"

if not DB_PATH.exists():
    raise FileNotFoundError(
        "Database not found. Run src\\load_database.py first."
    )

checks = []

def add_check(name, passed, details):
    checks.append({
        "Check": name,
        "Result": "PASS" if passed else "FAIL",
        "Details": str(details)
    })

with sqlite3.connect(DB_PATH) as con:
    orders = pd.read_sql_query("SELECT * FROM orders", con)
    products = pd.read_sql_query("SELECT * FROM products", con)
    customers = pd.read_sql_query("SELECT * FROM customers", con)
    inventory = pd.read_sql_query("SELECT * FROM inventory", con)
    suppliers = pd.read_sql_query("SELECT * FROM suppliers", con)
    deliveries = pd.read_sql_query(
        "SELECT * FROM supplier_deliveries", con
    )

# 1. Required tables have data
for name, df in {
    "orders": orders,
    "products": products,
    "customers": customers,
    "inventory": inventory,
    "suppliers": suppliers,
    "supplier_deliveries": deliveries
}.items():
    add_check(
        f"{name} is not empty",
        not df.empty,
        f"{len(df)} rows"
    )

# 2. Primary keys are unique
for name, df, key in [
    ("products", products, "ProductID"),
    ("customers", customers, "CustomerID"),
    ("suppliers", suppliers, "SupplierID"),
    ("inventory", inventory, "ProductID")
]:
    duplicates = int(df[key].duplicated().sum())
    add_check(
        f"{name}.{key} is unique",
        duplicates == 0,
        f"{duplicates} duplicate keys"
    )

# 3. Orders refer to existing products and customers
unknown_products = int(
    (~orders["ProductID"].isin(products["ProductID"])).sum()
)
unknown_customers = int(
    (~orders["CustomerID"].isin(customers["CustomerID"])).sum()
)

add_check(
    "Order product references are valid",
    unknown_products == 0,
    f"{unknown_products} unknown product references"
)
add_check(
    "Order customer references are valid",
    unknown_customers == 0,
    f"{unknown_customers} unknown customer references"
)

# 4. Order financial calculations
cancelled = orders["Status"].eq("Cancelled")
active = orders.loc[~cancelled]

revenue_errors = int((
    (active["GrossSales"] - active["DiscountAmount"])
    - active["NetRevenue"]
).abs().gt(0.01).sum())

profit_errors = int((
    (
        active["NetRevenue"]
        - active["ProductCost"]
        - active["ShippingCost"]
    )
    - active["GrossProfit"]
).abs().gt(0.01).sum())

add_check(
    "Net revenue formula",
    revenue_errors == 0,
    f"{revenue_errors} mismatches"
)
add_check(
    "Gross profit formula",
    profit_errors == 0,
    f"{profit_errors} mismatches"
)

# 5. Inventory references and basic values
unknown_inventory_products = int(
    (~inventory["ProductID"].isin(products["ProductID"])).sum()
)
add_check(
    "Inventory product references are valid",
    unknown_inventory_products == 0,
    f"{unknown_inventory_products} unknown products"
)

negative_stock = int((inventory["StockOnHand"] < 0).sum())
add_check(
    "Inventory stock is non-negative",
    negative_stock == 0,
    f"{negative_stock} negative stock values"
)

# 6. Supplier references in deliveries
unknown_delivery_suppliers = int(
    (~deliveries["SupplierID"].isin(suppliers["SupplierID"])).sum()
)
add_check(
    "Delivery supplier references are valid",
    unknown_delivery_suppliers == 0,
    f"{unknown_delivery_suppliers} unknown suppliers"
)

# Save and display report
report = pd.DataFrame(checks)
report_path = BASE_DIR / "data" / "processed" / "quality_report.csv"
report.to_csv(report_path, index=False)

print("\nOMNICHAIN INTELLIGENCE - QUALITY REPORT")
print("=" * 60)
print(report.to_string(index=False))

print("\nPassed:", (report["Result"] == "PASS").sum())
print("Failed:", (report["Result"] == "FAIL").sum())
print("Report saved to:", report_path)
