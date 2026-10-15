
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "omnichain.db"
EXPORT_DIR = BASE_DIR / "data" / "powerbi"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

tables = [
    "orders",
    "products",
    "customers",
    "inventory",
    "suppliers",
    "supplier_deliveries",
]

if not DB_PATH.exists():
    raise FileNotFoundError(
        f"Database not found: {DB_PATH}"
    )

with sqlite3.connect(DB_PATH) as connection:
    for table in tables:
        df = pd.read_sql_query(
            f'SELECT * FROM "{table}"',
            connection
        )

        output_path = EXPORT_DIR / f"{table}.csv"
        df.to_csv(output_path, index=False)

        print(f"Exported {table}: {len(df)} rows")

print("\nAll CSV files exported successfully.")
print(f"Folder: {EXPORT_DIR}")
