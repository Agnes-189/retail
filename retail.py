import sqlite3
from pathlib import Path

import pandas as pd


def main():
    db_path = Path(__file__).resolve().with_name("retail_sales.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores(
        store_id INTEGER PRIMARY KEY,
        store_name TEXT NOT NULL,
        region TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        sale_date TEXT NOT NULL,
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
    )
    """)

    stores = [
        (1, "Store A", "North"),
        (2, "Store B", "South"),
        (3, "Store C", "East"),
        (4, "Store D", "West")
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO stores (store_id, store_name, region) VALUES (?, ?, ?)",
        stores
    )

    sales = [
        (1, 1, 1000.50, "2026-01-15"),
        (2, 2, 1500.75, "2026-01-16"),
        (3, 3, 2000.00, "2026-01-17"),
        (4, 4, 7289.57, "2026-01-18"),
        (5, 1, 3200.58, "2026-01-20"),
        (6, 4, 6500.59, "2026-01-21"),
        (7, 3, 4300.60, "2025-01-22"),
        (8, 2, 3600.62, "2025-01-23"),
        (9, 3, 5100.63, "2025-02-10"),
        (10, 1, 5000.47, "2025-02-11")
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO sales (sale_id, store_id, amount, sale_date) VALUES (?, ?, ?, ?)",
        sales
    )

    conn.commit()

    query = """
    SELECT
        st.store_name,
        st.region,
        SUM(sa.amount) AS total_sales,
        COUNT(sa.sale_id) AS sales_count
    FROM sales sa
    INNER JOIN stores st ON st.store_id = sa.store_id
    WHERE st.region IN ('North', 'West')
      AND sa.sale_date LIKE '2026-01%'
    GROUP BY st.store_name, st.region
    HAVING SUM(sa.amount) > 5000
    ORDER BY total_sales DESC
    """

    result = pd.read_sql_query(query, conn)
    print("--- SQL Query Result ---")
    print(result)

    conn.close()


if __name__ == "__main__":
    main()
