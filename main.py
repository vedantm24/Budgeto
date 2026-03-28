import sys

"""Budgeto command-line entrypoint.

This module shows the main menu and routes each user selection to the
appropriate expense management or AI analysis workflow.
"""

from add_expense import add_expenses
from view_expenses import view_expenses
from ai_analysis import run_ai_analysis


def print_menu():
    # Show the main menu options available to the user.
    print("\nBudgeto - Main Menu")
    print("1. Add expenses")
    print("2. View expenses")
    print("3. Run AI analysis")
    print("4. Quit")


def main():
    while True:
        print_menu()
        choice = input("Select an option [1-4]: ").strip()

        # Dispatch the selected menu action.
        if choice == "1":
            add_expenses()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            run_ai_analysis()
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    # Run the app and handle keyboard interrupts cleanly.
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled by user. Exiting.")
        sys.exit(0)
