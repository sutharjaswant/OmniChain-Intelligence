# OmniChain Intelligence

A portfolio project demonstrating supply-chain analytics using **synthetic demonstration data**.

## Dataset disclaimer
All generated records are simulated. Inventory snapshots, supplier deliveries, costs, and sales are examples for demonstrating analytics, not real company records.

## Setup (Windows CMD)
```cmd
cd /d C:\OmniChain-Intelligence
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python src\generate_data.py
```

## Generated tables
- `data/raw/orders.csv`
- `data/raw/products.csv`
- `data/raw/customers.csv`
- `data/raw/inventory.csv`
- `data/raw/suppliers.csv`
- `data/raw/supplier_deliveries.csv`

Build and validate these tables before creating the dashboard.
