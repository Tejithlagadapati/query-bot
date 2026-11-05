import sqlite3

from app.config import DB_PATH

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def initialize_database():
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendors (
                vendor_id INTEGER PRIMARY KEY,
                vendor_name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY,
                vendor_id INTEGER NOT NULL,
                department TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount >= 0),
                expense_date TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                budget_id INTEGER PRIMARY KEY,
                department TEXT NOT NULL,
                category TEXT NOT NULL,
                budget_amount REAL NOT NULL CHECK (budget_amount >= 0),
                UNIQUE (department, category)
            )
        """)

        cursor.executemany("""
            INSERT OR IGNORE INTO vendors (vendor_id, vendor_name, category)
            VALUES (?, ?, ?)
        """, [
            (1, "CloudNova", "Cloud Services"),
            (2, "DevTools Pro", "Software"),
            (3, "OfficeHub", "Office Supplies"),
            (4, "SecureNet", "Security"),
        ])

        cursor.executemany("""
            INSERT OR IGNORE INTO expenses
                (expense_id, vendor_id, department, category,
                 amount, expense_date, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (1, 1, "Engineering", "Cloud", 12000.00, "2026-07-05", "Cloud hosting"),
            (2, 2, "Engineering", "Software", 8500.00, "2026-07-12", "Developer subscriptions"),
            (3, 1, "Data", "Cloud", 9500.00, "2026-08-03", "Model experimentation"),
            (4, 2, "Engineering", "Software", 7200.00, "2026-08-15", "Development tools"),
            (5, 3, "Operations", "Office", 2400.00, "2026-08-20", "Office supplies"),
            (6, 4, "Security", "Software", 6000.00, "2026-09-02", "Security software"),
            (7, 2, "Data", "Software", 5100.00, "2026-09-10", "Data team subscriptions"),
            (8, 1, "Engineering", "Cloud", 14000.00, "2026-10-04", "Cloud hosting"),
            (9, 2, "Engineering", "Software", 15000.00, "2026-09-18", "Annual IDE licences"),
            (10, 4, "Security", "Software", 11000.00, "2026-08-25", "Endpoint protection licences"),
        ])

        cursor.executemany("""
            INSERT OR IGNORE INTO budgets
                (budget_id, department, category, budget_amount)
            VALUES (?, ?, ?, ?)
        """, [
            (1, "Engineering", "Software", 20000.00),
            (2, "Engineering", "Cloud", 30000.00),
            (3, "Data", "Software", 12000.00),
            (4, "Data", "Cloud", 20000.00),
            (5, "Operations", "Office", 5000.00),
            (6, "Security", "Software", 8000.00),
        ])

        connection.commit()
        print("Database initialized:", DB_PATH)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()