from datetime import datetime
from add_expense import list_expenses, filter_expenses_by_category, filter_expenses_by_date, update_expense


def _print_expense(e, index=None):
    prefix = f"{index}. " if index is not None else "- "
    print(f"{prefix}{e['date']} | {e['category']} | ₹{e['amount']:.2f} | {e['description']}")


def _select_expense_index():
    items = list_expenses()
    if not items:
        print("No expenses available.")
        return None

    for idx, exp in enumerate(items):
        _print_expense(exp, idx)

    sel = input("Enter expense index to update: ").strip()
    if not sel.isdigit():
        print("Invalid index.")
        return None

    idx = int(sel)
    if idx < 0 or idx >= len(items):
        print("Index out of range.")
        return None

    return idx


def view_expenses():
    """Interactive view and filter expenses workflow."""
    print("\nView expenses")
    print("1. List all")
    print("2. Filter by category")
    print("3. Filter by date")
    print("4. Update expense")
    print("5. Back")

    choice = input("Select an option [1-5]: ").strip()

    if choice == "1":
        items = list_expenses()
        print(f"\nTotal expenses: {len(items)}")
        for exp in items:
            _print_expense(exp)

    elif choice == "2":
        category = input("Category name: ").strip()
        if not category:
            print("Category required")
            return
        items = filter_expenses_by_category(category)
        print(f"\n{len(items)} expenses in category '{category}'")
        for exp in items:
            _print_expense(exp)

    elif choice == "3":
        date_input = input("Date (YYYY-MM-DD): ").strip()
        if not date_input:
            print("Date required")
            return
        try:
            items = filter_expenses_by_date(date_input)
        except ValueError as exc:
            print(str(exc))
            return
        print(f"\n{len(items)} expenses on {date_input}")
        for exp in items:
            _print_expense(exp)

    elif choice == "4":
        idx = _select_expense_index()
        if idx is None:
            return

        current = list_expenses()[idx]
        print("Leave blank to keep the current value")

        amount_input = input(f"Amount [{current['amount']}]: ").strip()
        category_input = input(f"Category [{current['category']}]: ").strip()
        date_input = input(f"Date [{current['date']} - YYYY-MM-DD]: ").strip()
        description_input = input(f"Description [{current['description']}]: ").strip()

        amount = float(amount_input) if amount_input else current["amount"]
        category = category_input if category_input else current["category"]

        if date_input:
            try:
                parsed_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. No change applied.")
                parsed_date = current["date"]
        else:
            parsed_date = current["date"]

        description = description_input if description_input else current["description"]

        updated = update_expense(idx, amount=amount, category=category, date=parsed_date, description=description)
        print("Updated expense:", updated)

    elif choice == "5":
        return
    else:
        print("Invalid choice")
