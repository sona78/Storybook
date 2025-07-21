from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from clients import supabase

app = Flask(__name__)


def add_agent_entry(content: str, image_prompt: str, image_url: str, datetime: datetime):
    """
    Use this tool to add a new entry to the agent database.
    Provide the text content you want to record.
    Each new entry gets a date_incremental_id that starts from 0 for each day.
    """

    with app.app_context():
        
        try:
            story_data = {
                "content": content,
                "datetime": datetime.isoformat(),
                "image_prompt": image_prompt,
                "image_url": image_url
            }
            # Select the table and insert the data
            data, count = supabase.table('storybook').insert(story_data).execute()

            # The 'data' variable contains a list with the inserted record
            print(story_data)
            # print(data[1]) # The actual data is in the second element of the tuple

        except Exception as e:
            print(f"Error: Could not add entry to database. Details: {e}")




def create_combined_prompt() -> str:
    """
    Combines all content in the agent database in array order (by date, then date_incremental_id) and returns as a single string.
    """
    with app.app_context():
        response = (
            supabase.table("storybook")
            .select("content")
            .execute()
        )
        # The response is expected to have a 'data' attribute which is a list of dicts like [{'content': '...'}, ...]
        if hasattr(response, 'data') and response.data:
            contents = [entry['content'] for entry in response.data if 'content' in entry]
            return " ".join(contents)
        else:
            return ""
            

def get_storybook():
    with app.app_context():
        try:
            entries = (
                supabase.table("storybook")
                .select("*")
                .execute()
            ).data
            if not entries:
                print("No entries found in the database.")
                return []
            return entries
        except Exception as e:
            print(f"Error: Could not see entries in database. Details: {e}")
            return []