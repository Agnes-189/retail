import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('dailysales.db')
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS stores (
    store_id INTEGER PRIMARY KEY,
    store_name TEXT NOT NULL,
    region TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_reps (
    rep_id TEXT PRIMARY KEY,
    rep_name TEXT NOT NULL,
    store_id INTEGER NOT NULL,
    commission_rate REAL NOT NULL,
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_data (
    sales_id INTEGER PRIMARY KEY,
    store_id INTEGER NOT NULL,
    rep_id TEXT NOT NULL,
    amount REAL NOT NULL,
    sales_date TEXT NOT NULL,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
)
""")

# Insert sample data
stores = [
    (101, "Ziped", "Nairobi"),
    (102, "Hyped", "Mombasa"),
    (103, "Jpye", "Nyeri"),
    (104, "Skig", "Nakuru")
]

cursor.executemany(
    "INSERT OR REPLACE INTO stores (store_id, store_name, region) VALUES (?, ?, ?)",
    stores
)

sales_reps = [
    ("R01", "Alex Mercer", 101, 0.05),
    ("R02", "Dana Scully", 102, 0.07),
    ("R03", "Fox Mulder", 101, 0.06)
]

cursor.executemany(
    "INSERT OR REPLACE INTO sales_reps (rep_id, rep_name, store_id, commission_rate) VALUES (?, ?, ?, ?)",
    sales_reps
)

sales_data = [
    (1, 101, "R01", 1500.00, "2026-01-10"),
    (2, 101, "R03", 2500.00, "2026-01-12"),
    (3, 102, "R02", 4000.00, "2026-01-15"),
    (4, 101, "R01", 3000.00, "2026-01-20")
]

cursor.executemany(
    "INSERT OR REPLACE INTO sales_data (sales_id, store_id, rep_id, amount, sales_date) VALUES (?, ?, ?, ?, ?)",
    sales_data
)

conn.commit()

# Query joined data
query = """
SELECT
    sr.rep_name,
    st.store_name,
    SUM(sd.amount) AS total_sales,
    SUM(sd.amount * sr.commission_rate) AS commission_earned
FROM sales_data sd
JOIN sales_reps sr ON sd.rep_id = sr.rep_id
JOIN stores st ON sd.store_id = st.store_id
WHERE sd.sales_date LIKE '2026%'
GROUP BY sr.rep_name, st.store_name
ORDER BY commission_earned DESC
"""

result = pd.read_sql_query(query, conn)
print(result)

conn.close()