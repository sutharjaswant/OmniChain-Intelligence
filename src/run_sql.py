
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "omnichain.db"
SQL_PATH = BASE_DIR / "sql" / "01_business_analysis.sql"

if not DB_PATH.exists():
    raise FileNotFoundError("Database not found. Run load_database.py first.")

if not SQL_PATH.exists():
    raise FileNotFoundError("SQL file not found in the sql folder.")

sql_text = SQL_PATH.read_text(encoding="utf-8")

# Split the SQL file into individual statements
queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

with sqlite3.connect(DB_PATH) as connection:
    print("OMNICHAIN INTELLIGENCE - SQL ANALYSIS")
    print("=" * 50)

    for number, query in enumerate(queries, start=1):
        # Skip comment-only statements
        cleaned_lines = [
            line for line in query.splitlines()
            if line.strip() and not line.strip().startswith("--")
        ]

        if not cleaned_lines:
            continue

        executable_query = "\n".join(cleaned_lines)

        try:
            result = pd.read_sql_query(
                executable_query, connection
            )

            print(f"\nQUERY {number}")
            print("-" * 50)

            if result.empty:
                print("No rows returned.")
            else:
                print(result.to_string(index=False))

        except Exception as error:
            print(f"\nQUERY {number} FAILED")
            print(error)
            raise

print("\nAll SQL queries executed successfully.")
