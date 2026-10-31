import sqlite3
from pathlib import Path

# Resolve path directly to the data folder
QUERYPILOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = QUERYPILOT_DIR / "data" / "querypilot.db"


def get_total_spending(category: str, start_date: str, end_date: str) -> float:
    query = """
        SELECT COALESCE(SUM(amount), 0.0) AS total
        FROM expenses
        WHERE category = ?
          AND expense_date >= ?
          AND expense_date <= ?
    """
    # Use the dynamic arguments passed to the function!
    params = (category, start_date, end_date)

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        result = cursor.execute(query, params).fetchone()
        return result[0]


# Test 1: Software spending
software_total = get_total_spending("Software", "2026-07-01", "2026-09-30")
print(f"Software total: {software_total}")

# Test 2: Cloud spending (Now this actually works!)
cloud_total = get_total_spending("Cloud", "2026-07-01", "2026-10-31")
print(f"Cloud total: {cloud_total}")
