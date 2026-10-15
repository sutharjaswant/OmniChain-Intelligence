
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "omnichain.db"

if not DB_PATH.exists():
    raise FileNotFoundError(
        "Database not found. Run src\\load_database.py first."
    )

with sqlite3.connect(DB_PATH) as connection:
    tables = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

    print("DATABASE TABLES")
    for (table_name,) in tables:
        count = connection.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        ).fetchone()[0]
        print(f"{table_name}: {count} rows")

    print("\nSAMPLE REVENUE SUMMARY")
    result = connection.execute("""
        SELECT
            COUNT(*) AS total_orders,
            ROUND(SUM(NetRevenue), 2) AS total_net_revenue,
            ROUND(SUM(GrossProfit), 2) AS total_gross_profit
        FROM orders
    """).fetchone()

    print("Total orders:", result[0])
    print("Net revenue:", result[1])
    print("Gross profit:", result[2])

print("\nDatabase verification completed.")
