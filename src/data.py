"""
Generate clearly labeled synthetic data for the OmniChain Intelligence demo.
All records and operational metrics are simulated, not real company data.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(42)

categories = ["Electronics", "Home & Kitchen", "Office Supplies", "Outdoor", "Personal Care"]
n_products, n_suppliers, n_customers, n_orders = 60, 12, 180, 1800
products = pd.DataFrame({
    "ProductID": [f"P{i:04d}" for i in range(1, n_products + 1)],
    "ProductName": [f"Product {i:03d}" for i in range(1, n_products + 1)],
    "Category": rng.choice(categories, n_products),
    "UnitCost": np.round(rng.uniform(4, 180, n_products), 2),
    "SupplierID": rng.choice([f"S{i:03d}" for i in range(1, n_suppliers + 1)], n_products)
})
products["ListPrice"] = np.round(products["UnitCost"] * rng.uniform(1.25, 2.15, n_products), 2)
products.to_csv(RAW / "products.csv", index=False)

suppliers = pd.DataFrame({
    "SupplierID": [f"S{i:03d}" for i in range(1, n_suppliers + 1)],
    "SupplierName": [f"Supplier {i:02d}" for i in range(1, n_suppliers + 1)],
    "Region": rng.choice(["North", "South", "East", "West", "Central"], n_suppliers),
    "ContractLeadTimeDays": rng.integers(3, 19, n_suppliers),
    "TargetOnTimeRate": np.round(rng.uniform(0.88, 0.99, n_suppliers), 3)
})
suppliers.to_csv(RAW / "suppliers.csv", index=False)

customers = pd.DataFrame({
    "CustomerID": [f"C{i:05d}" for i in range(1, n_customers + 1)],
    "Region": rng.choice(["North", "South", "East", "West", "Central"], n_customers)
})
customers.to_csv(RAW / "customers.csv", index=False)

rng_dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n_orders), unit="D")
product_idx = rng.integers(0, n_products, n_orders)
quantity = rng.integers(1, 13, n_orders)
discount = np.round(rng.choice([0, .05, .10, .15, .20], n_orders, p=[.40, .20, .22, .13, .05]), 2)
orders = pd.DataFrame({
    "OrderID": [f"O{i:06d}" for i in range(1, n_orders + 1)],
    "OrderDate": rng_dates,
    "CustomerID": rng.choice(customers["CustomerID"], n_orders),
    "ProductID": products.iloc[product_idx]["ProductID"].to_numpy(),
    "Quantity": quantity,
    "DiscountRate": discount,
    "ShippingCost": np.round(rng.uniform(1.5, 24, n_orders), 2),
    "Status": rng.choice(["Delivered", "Delivered", "Delivered", "Returned", "Cancelled"], n_orders, p=[.65, .16, .10, .06, .03])
})
orders = orders.merge(products[["ProductID", "UnitCost", "ListPrice"]], on="ProductID", how="left")
orders["GrossSales"] = orders["Quantity"] * orders["ListPrice"]
orders["DiscountAmount"] = orders["GrossSales"] * orders["DiscountRate"]
orders["NetRevenue"] = orders["GrossSales"] - orders["DiscountAmount"]
orders["ProductCost"] = orders["Quantity"] * orders["UnitCost"]
orders["GrossProfit"] = orders["NetRevenue"] - orders["ProductCost"] - orders["ShippingCost"]
cancelled = orders["Status"].eq("Cancelled")
orders.loc[cancelled, ["GrossSales", "DiscountAmount", "NetRevenue", "ProductCost", "GrossProfit"]] = 0
orders["OrderDate"] = orders["OrderDate"].dt.strftime("%Y-%m-%d")
orders = orders.drop(columns=["UnitCost", "ListPrice"])
orders.to_csv(RAW / "orders.csv", index=False)

inventory = products[["ProductID", "SupplierID"]].copy()
inventory["StockOnHand"] = rng.integers(0, 260, n_products)
inventory["ReorderPoint"] = rng.integers(25, 90, n_products)
inventory["DailyDemandEstimate"] = np.round(rng.uniform(0.5, 8.0, n_products), 2)
inventory["SnapshotDate"] = "2025-12-31"
inventory["StockStatus"] = np.select(
    [inventory["StockOnHand"] <= inventory["ReorderPoint"],
     inventory["StockOnHand"] >= inventory["ReorderPoint"] * 2.5],
    ["Reorder", "Excess"], default="Healthy")
inventory.to_csv(RAW / "inventory.csv", index=False)

delivery_rows = []
for _, s in suppliers.iterrows():
    for j in range(1, 41):
        order_date = pd.Timestamp("2025-01-01") + pd.Timedelta(days=int(rng.integers(0, 340)))
        lead = int(max(1, rng.normal(float(s["ContractLeadTimeDays"]) + 1.5, 4)))
        delivered = order_date + pd.Timedelta(days=lead)
        delivery_rows.append({
            "DeliveryID": f"D{s['SupplierID'][1:]}-{j:03d}",
            "SupplierID": s["SupplierID"],
            "OrderDate": order_date.strftime("%Y-%m-%d"),
            "DeliveredDate": delivered.strftime("%Y-%m-%d"),
            "ActualLeadTimeDays": lead,
            "OnTime": lead <= int(s["ContractLeadTimeDays"]),
            "DefectRate": round(float(rng.uniform(0, .08)), 3)
        })
pd.DataFrame(delivery_rows).to_csv(RAW / "supplier_deliveries.csv", index=False)

print("Synthetic demo datasets created in data/raw/")
for file in sorted(RAW.glob("*.csv")):
    frame = pd.read_csv(file)
    print(f"{file.name}: {len(frame):,} rows, {len(frame.columns)} columns")
print("NOTICE: all records are simulated demonstration data.")
