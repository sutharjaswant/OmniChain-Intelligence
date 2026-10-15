
from pathlib import Path
import sqlite3
import pandas as pd

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Support either data/ or data/raw/
if not (DATA_DIR / "orders.csv").exists():
    DATA_DIR = DATA_DIR / "raw"

DB_DIR = BASE_DIR / "data" / "processed"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "omnichain.db"

# CSV files and their corresponding SQL table names
FILES = {
    "orders": "orders.csv",
    "products": "products.csv",
    "customers": "customers.csv",
    "inventory": "inventory.csv",
    "suppliers": "suppliers.csv",
    "supplier_deliveries": "supplier_deliveries.csv",
}

def main():
    # Check all input files before creating the database
    missing_files = [
        filename
        for filename in FILES.values()
        if not (DATA_DIR / filename).exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Missing CSV files in {DATA_DIR}: {missing_files}"
        )

    print("Loading OmniChain Intelligence data...")
    print(f"CSV folder: {DATA_DIR}")

    with sqlite3.connect(DB_PATH) as connection:
        for table_name, filename in FILES.items():
            file_path = DATA_DIR / filename
            df = pd.read_csv(file_path)

            # Replace the table each time the loader is run
            df.to_sql(
                table_name,
                connection,
                if_exists="replace",
                index=False
            )

            # Verify the number of rows stored in SQLite
            row_count = connection.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]

            print(f"{table_name}: {row_count} rows loaded")

    print("\nDatabase created successfully.")
    print(f"Location: {DB_PATH}")

if __name__ == "__main__":
    main()
