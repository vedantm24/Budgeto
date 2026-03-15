# Budgeto

Budgeto is a simple command-line personal finance tracker with support for:
- Add expenses (amount, category, date, description)
- View expenses (list, filter by category or date)
- Update existing expenses
- Persist expenses to `expenses.json`
- Basic AI-driven budget analysis (OpenAI + HuggingFace router)

## Project structure

- `main.py` - command menu with actions: add, view, AI analysis, quit
- `add_expense.py` - in-memory expense store + add helpers + persistence logic
- `view_expenses.py` - viewing + filters + update workflow
- `storage.py` - JSON load/save for expenses
- `ai_analysis.py` - AI budget analysis prompt and model call
- `.env` - supports `API_KEY` for OpenAI/HuggingFace

## Setup

1. Install dependencies
   ```powershell
   pip install openai python-dotenv
   ```
2. Create `.env` in repository root:
   ```ini
   API_KEY=your_api_key_here
   ```

## Usage

Run app:
```powershell
python main.py
```

Menu options:
1. Add expenses
2. View expenses
3. Run AI analysis
4. Quit

### Add expense
- Prompts for amount, category, date (YYYY-MM-DD), description
- Saves to memory and `expenses.json`

### View expenses
- List all
- Filter by category
- Filter by date
- Update expense by index

### AI analysis
- Summarizes spending
- Recommends top cost categories and a 4-week budget
- Uses task prompt in `ai_analysis.py`

## Notes

- Expenses are stored in-memory and synced to `expenses.json`.
- Update is based on index (0-based from listing).
- Make sure `API_KEY` is valid for AI analysis.

## Troubleshooting

- If AI analysis fails, verify `.env` `API_KEY` and network connectivity.
- If expense outputs show `₹`, this is intended currency format.
