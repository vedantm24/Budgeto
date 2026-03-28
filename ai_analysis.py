import os
from openai import OpenAI
from dotenv import load_dotenv
from view_expenses import list_expenses

"""AI budget analysis helpers.

Uses expenses loaded by the app and sends them to an OpenAI-compatible model
for spending summary and budget recommendations.
"""

load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("API_KEY")
)


def run_ai_analysis(list_expenses_func=list_expenses):
    """Run AI analysis using expenses list and return model response."""
    expenses = list_expenses_func()
    # Ensure there is valid expense data before calling the AI model.
    if not isinstance(expenses, list) or not expenses:
        print("No expenses data found for AI analysis.")
        return

    # Build prompt content for budget analysis
    content = (
        "You are a financial assistant. Analyze the given expenses and build a budget.\n\n"
        "Data format is a JSON list with amount, category, date (YYYY-MM-DD), description.\n"
        "Tasks:\n"
        "1) Summarize total spending and spending per category.\n"
        "2) Identify top 3 expense categories.\n"
        "3) Propose a 4-week budget with savings target.\n"
        "4) Give practical cost reduction recommendations.\n"
        "5) Present a simple monthly budget template.\n\n"
        f"Here are the expense records:\n{expenses}\n"
    )

    # Send the budget analysis task and expense data to the AI model.
    try:
        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            temperature=0.7,
            max_tokens=800,
        )
    except Exception as e:
        print("AI analysis request failed:", e)
        return None

    response_text = None
    try:
        choices = getattr(completion, "choices", None)
        if not choices:
            raise ValueError("No choices returned by the model.")

        first_choice = choices[0]
        if isinstance(first_choice, dict):
            response_text = first_choice.get("message", {}).get("content")
        else:
            message = getattr(first_choice, "message", None)
            response_text = getattr(message, "content", None) if message is not None else None

        if not response_text:
            raise ValueError("Model response is empty or malformed.")

    except Exception as e:
        print("AI analysis failed to parse model output:", e)
        return None

    print("AI analysis result:\n", response_text)
    return response_text

