import json
from datetime import datetime
from pathlib import Path

"""JSON persistence helpers for Budgeto expenses."""

DEFAULT_EXPENSES_FILE = Path("expenses.json")


def _serialize_expense(expense):
    """Convert an expense record into JSON-serializable form."""
    return {
        "amount": expense["amount"],
        "category": expense["category"],
        "date": expense["date"].isoformat() if hasattr(expense["date"], "isoformat") else str(expense["date"]),
        "description": expense.get("description", ""),
    }


def _deserialize_expense(data):
    """Convert raw JSON data into a normalized expense record."""
    d = {
        "amount": float(data["amount"]),
        "category": str(data.get("category", "")).strip(),
        "date": datetime.strptime(str(data["date"]), "%Y-%m-%d").date(),
        "description": str(data.get("description", "")).strip(),
    }
    return d


def load_expenses(file_path=None):
    """Load expenses from JSON file and return list of dicts."""
    path = Path(file_path) if file_path else DEFAULT_EXPENSES_FILE
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
            if not isinstance(payload, list):
                raise ValueError("Invalid format: expected a list")
            return [_deserialize_expense(item) for item in payload]
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in {path}")


def save_expenses(expenses, file_path=None):
    """Persist expenses list to JSON file."""
    path = Path(file_path) if file_path else DEFAULT_EXPENSES_FILE
    path.parent.mkdir(parents=True, exist_ok=True)

    serial = [_serialize_expense(exp) for exp in expenses]
    with path.open("w", encoding="utf-8") as f:
        json.dump(serial, f, indent=2, ensure_ascii=False)
