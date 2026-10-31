
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_DIR / "data" / "querypilot.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_total_spending(start_date, end_date, category=None):
    """Calculate spending between two inclusive dates."""

    query = """
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE expense_date >= ?
          AND expense_date <= ?
    """
    params = [start_date, end_date]

    if category is not None:
        query += " AND category = ?"
        params.append(category)

    with get_connection() as connection:
        row = connection.execute(query, params).fetchone()
        return row["total"]


def get_department_spending(start_date, end_date):
    """Return spending totals grouped by department."""

    query = """
        SELECT department, SUM(amount) AS total
        FROM expenses
        WHERE expense_date >= ?
          AND expense_date <= ?
        GROUP BY department
        ORDER BY total DESC
    """

    with get_connection() as connection:
        rows = connection.execute(
            query, (start_date, end_date)
        ).fetchall()
        return [dict(row) for row in rows]


def get_budget_status(department, category):
    """Compare all recorded spending with a department's budget."""

    query = """
        SELECT
            b.department,
            b.category,
            b.budget_amount,
            COALESCE(SUM(e.amount), 0) AS total_spent
        FROM budgets AS b
        LEFT JOIN expenses AS e
          ON e.department = b.department
         AND e.category = b.category
        WHERE b.department = ?
          AND b.category = ?
        GROUP BY b.budget_id, b.department, b.category, b.budget_amount
    """

    with get_connection() as connection:
        row = connection.execute(
            query, (department, category)
        ).fetchone()

        if row is None:
            return None

        result = dict(row)
        result["remaining"] = (
            result["budget_amount"] - result["total_spent"]
        )
        result["over_budget"] = result["total_spent"] > result["budget_amount"]
        return result
