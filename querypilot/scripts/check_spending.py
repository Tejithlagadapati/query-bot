import sqlite3

from app.config import DB_PATH


def get_total_spending(category, start_date, end_date):
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE category = ?
              AND expense_date BETWEEN ? AND ?
        """, (category, start_date, end_date))
        total = cursor.fetchone()[0]
        return total if total is not None else 0.0
    finally:
        connection.close()


if __name__ == "__main__":
    result = get_total_spending("Cloud", "2026-07-01", "2026-09-30")
    print(f"Total cloud spending: {result}")