import os
from openai import OpenAI
from dotenv import load_dotenv
from view_expenses import list_expenses

load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("API_KEY")
)


def run_ai_analysis(list_expenses_func=list_expenses):
    """Run AI analysis using expenses list and return model response."""
    expenses = list_expenses_func()
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

    try:
        response_text = completion.choices[0].message.content
        print("AI analysis result:\n", response_text)
        
    except Exception as e:
        print("AI analysis failed:", e)

    return response_text

