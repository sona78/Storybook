from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, date

# This setup is just to configure SQLAlchemy, not to run a web server.
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'agent_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database table structure as an array with per-day incremental ids
class AgentEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.Date, nullable=False)
    date_incremental_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<AgentEntry id={self.id} content={self.content} date={self.date} date_incremental_id={self.date_incremental_id}>"

def get_entry_id_by_content(content: str):
    """
    Search for a specific content and retrieve its id.
    Returns the id if found, else None.
    """
    with app.app_context():
        entry = AgentEntry.query.filter_by(content=content).first()
        if entry:
            return entry.id
        else:
            return None

def add_agent_entry(content: str) -> str:
    """
    Use this tool to add a new entry to the agent database.
    Provide the text content you want to record.
    Each new entry gets a date_incremental_id that starts from 0 for each day.
    """
    try:
        with app.app_context():
            today = date.today()
            # Find the max date_incremental_id for today
            last_entry = (
                AgentEntry.query.filter_by(date=today)
                .order_by(AgentEntry.date_incremental_id.desc())
                .first()
            )
            if last_entry is None:
                new_date_incremental_id = 0
            else:
                new_date_incremental_id = last_entry.date_incremental_id + 1

            new_entry = AgentEntry(
                content=content,
                date=today,
                date_incremental_id=new_date_incremental_id
            )
            db.session.add(new_entry)
            db.session.commit()
            return (
                f"Success! Entry with global ID {new_entry.id}, date {today}, "
                f"date_incremental_id {new_entry.date_incremental_id} was added."
            )
    except Exception as e:
        return f"Error: Could not add entry to database. Details: {e}"

def create_combined_prompt():
    """
    Combines all content in the agent database in array order (by date, then date_incremental_id) and returns as a single string.
    """
    with app.app_context():
        entries = (
            AgentEntry.query.order_by(AgentEntry.date.asc(), AgentEntry.date_incremental_id.asc()).all()
        )
        if not entries:
            return ""
        contents = [entry.content for entry in entries]
        return "\n".join(contents)

def print_all_agent_entries():
    """
    Prints all entries in the agent database in array order (by date, then date_incremental_id).
    """
    with app.app_context():
        entries = (
            AgentEntry.query.order_by(AgentEntry.date.asc(), AgentEntry.date_incremental_id.asc()).all()
        )
        if not entries:
            print("No entries found in the database.")
            return
        for entry in entries:
            print(
                f"ID: {entry.id}, Content: {entry.content}, "
                f"Date: {entry.date}, Date Incremental ID: {entry.date_incremental_id}"
            )

# A helper function to ensure the database is created
def setup_database():
    with app.app_context():
        db.create_all()