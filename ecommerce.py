import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    np.random.seed(42)
    random.seed(42)

    db_path = Path(__file__).resolve().with_name("ecommerce.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id TEXT NOT NULL,
        order_date TEXT NOT NULL,
        order_amount REAL NOT NULL,
        status TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        delivery_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        carrier TEXT NOT NULL,
        delivery_days INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
    """)

    statuses = ["Completed", "Completed", "Completed", "Returned", "Pending"]
    carriers = ["DHL", "FedEx", "SpeedyExpress"]
    customers = [f"CUST_{i:03d}" for i in range(101, 120)]
    start_date = datetime(2026, 1, 1)

    order_rows = []
    delivery_rows = []

    for i in range(1, 26):
        c_id = random.choice(customers)
        o_date = (start_date + timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d")
        amount = round(random.uniform(25.0, 500.0), 2)
        status = random.choice(statuses)
        order_rows.append((i, c_id, o_date, amount, status))

        if status != "Pending":
            carrier = random.choice(carriers)
            days = random.randint(1, 7)
            delivery_rows.append((i, i, carrier, days))

    cursor.executemany("INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)", order_rows)
    cursor.executemany("INSERT OR REPLACE INTO deliveries VALUES (?, ?, ?, ?)", delivery_rows)
    conn.commit()

    query = """
    SELECT
        status,
        COUNT(*) AS order_count,
        ROUND(AVG(order_amount), 2) AS avg_amount
    FROM orders
    GROUP BY status
    ORDER BY order_count DESC
    """

    query1 = """
    SELECT
        carrier,
        COUNT(*) AS delivery_count,
        ROUND(AVG(delivery_days), 2) AS avg_days
    FROM deliveries
    GROUP BY carrier
    ORDER BY delivery_count DESC
    """

    result = pd.read_sql_query(query, conn)
    df_carrier = pd.read_sql_query(query1, conn)
    df_carrier = df_carrier[df_carrier["avg_days"] > 4.0].copy()

    print("Database 'ecommerce.db' populated successfully with 25 dynamic records.")
    print("=" * 60)
    print("Table 1: Orders by Status")
    print("=" * 60)
    print(result.to_string(index=False))
    print()
    print("=" * 60)
    print("Table 2: Deliveries by Carrier")
    print("=" * 60)
    print(df_carrier.to_string(index=False))

    if not df_carrier.empty:
        plt.figure(figsize=(7, 4))
        plt.bar(df_carrier["carrier"], df_carrier["delivery_count"], color="blue")
        plt.axhline(y=4.0, color="black", linestyle="--", label="SLA threshold")
        plt.title("Slow Carrier Summary")
        plt.xlabel("Carrier")
        plt.ylabel("Delivery Count")
        plt.legend()
        plt.tight_layout()
        plt.savefig("completed_deliveries.png")
        plt.close()
        plt.show()
        print("\nSaved chart to completed_deliveries.png")
    else:
        print("\nNo carriers exceeded the 4.0-day SLA threshold.")

    conn.close()


if __name__ == "__main__":
    main()