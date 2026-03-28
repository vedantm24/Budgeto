from datetime import datetime

from storage import load_expenses, save_expenses

"""Expense storage and interactive input helpers.

This module keeps an in-memory expense list loaded from disk at startup.
Add, update, delete, list, and filter operations update the persisted JSON file.
"""

# In-memory store for expenses, loaded from JSON file at startup.
expenses = load_expenses()  # each item is a dict with keys: amount, category, date, description


def _validate_date(date_text):
    """Parse a YYYY-MM-DD string into a date object or return None."""
    try:
        return datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        return None


def add_expense(amount, category, date, description):
    """Append a new expense record to the in-memory list and save to disk."""
    # Create a normalized expense record and store it persistently.
    record = {
        "amount": float(amount),
        "category": category.strip(),
        "date": date,
        "description": description.strip(),
    }
    expenses.append(record)
    save_expenses(expenses)
    return record


def update_expense(index, amount=None, category=None, date=None, description=None):
    """Update an expense record by index and save to disk."""
    if index < 0 or index >= len(expenses):
        raise IndexError("Expense index out of range")

    record = expenses[index]
    if amount is not None:
        record["amount"] = float(amount)
    if category is not None:
        record["category"] = category.strip()
    if date is not None:
        record["date"] = date
    if description is not None:
        record["description"] = description.strip()

    save_expenses(expenses)
    return record


def delete_expense(index):
    """Remove an expense record by index and save to disk."""
    if index < 0 or index >= len(expenses):
        raise IndexError("Expense index out of range")

    removed = expenses.pop(index)
    save_expenses(expenses)
    return removed


def list_expenses():
    """Return a copy of all expenses."""
    return list(expenses)


def filter_expenses_by_category(category):
    """Return expenses for a given category (case-insensitive)."""
    return [e for e in expenses if e["category"].lower() == category.strip().lower()]


def filter_expenses_by_date(date):
    """Return expenses for an exact date (datetime.date object or YYYY-MM-DD string)."""
    if isinstance(date, str):
        parsed_date = _validate_date(date)
        if parsed_date is None:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD")
        date = parsed_date

    return [e for e in expenses if e["date"] == date]


def add_expenses():
    """Interactive prompt for adding expenses from main menu."""
    print("\nAdd a new expense")
    
    amount_input = None
    while not amount_input:
        amount_input = input("\nAmount (e.g., 14.99): ").strip()
        if not amount_input:
            print("Error: amount is required.")
        else:
            try:
                amount = float(amount_input)
            except ValueError:
                print("Error: invalid amount. Please enter a number.")
                amount_input = None
            
    category = None
    while not category:
        category = input("\nCategory (e.g. groceries, utilities): ").strip()
        if not category:
            print("Error: category is required.")
    
    date_input = None
    while not date_input:
        date_input = input("\nDate (YYYY-MM-DD): ").strip()
        if not date_input:
            print("Error: date is required.")
        else:
            parsed_date = _validate_date(date_input)
            if parsed_date is None:
                print("Error: invalid date format. Use YYYY-MM-DD.")
                date_input = None

    description = input("\nDescription: ").strip()

    record = add_expense(amount, category, parsed_date, description)
    print("Added expense:", record)
