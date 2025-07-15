import os
from datetime import date

PROMPT_FILE = 'prompt_of_the_day.txt'
DATE_FILE = 'prompt_of_the_day_date.txt'

def set_prompt_of_the_day(prompt: str):
    """Set the prompt of the day and store today's date."""
    with open(PROMPT_FILE, 'w', encoding='utf-8') as f:
        f.write(prompt)
    with open(DATE_FILE, 'w', encoding='utf-8') as f:
        f.write(str(date.today()))

def get_prompt_of_the_day() -> str:
    """Get the prompt of the day. Returns empty string if not set or expired."""
    if not os.path.exists(PROMPT_FILE) or not os.path.exists(DATE_FILE):
        return ''
    with open(DATE_FILE, 'r', encoding='utf-8') as f:
        stored_date = f.read().strip()
    if stored_date != str(date.today()):
        return ''
    with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def reset_prompt_of_the_day():
    """Remove the prompt of the day (for a new day or admin reset)."""
    if os.path.exists(PROMPT_FILE):
        os.remove(PROMPT_FILE)
    if os.path.exists(DATE_FILE):
        os.remove(DATE_FILE) 