from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from langchain_core.tools import tool
import os

# This setup is just to configure SQLAlchemy, not to run a web server.
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'agent_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database table structure as a linked list
class AgentEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    next_id = db.Column(db.Integer, db.ForeignKey('agent_entry.id'), nullable=True)
    next = db.relationship('AgentEntry', remote_side=[id], uselist=False)

    def __repr__(self):
        return f"<AgentEntry id={self.id} agent_id={self.agent_id} content={self.content} next_id={self.next_id}>"

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

# This decorator turns our Python function into a "tool" the agent can use.
@tool
def add_agent_entry(agent_id: str, content: str, previousContent: str = "") -> str:
    """
    Use this tool to add a new entry to the agent database as a linked list.
    Provide the agent_id and the text content you want to record.
    If this is the first addition to the database, set id as 0 and next_id as None.
    Each new entry is appended to the end of the linked list.
    """
    try:
        with app.app_context():
            # Find the last entry in the linked list (where next_id is None)
            last_entry = AgentEntry.query.filter_by(next_id=None).order_by(AgentEntry.id.desc()).first()
            if not last_entry:
                # First entry: set id to 0 explicitly
                new_entry = AgentEntry(id=0, agent_id=agent_id, content=content, next_id=None)
                db.session.add(new_entry)
                db.session.commit()
                return f"Success! First entry with ID {new_entry.id} was added for agent {agent_id}."
            elif previousContent:
                prev_id = get_entry_id_by_content(previousContent)
                prev = AgentEntry.query.get(prev_id)
                if prev_id != None and prev != None:
                    new_entry = AgentEntry(agent_id=agent_id, content=content, next_id=prev.id)
                    db.session.add(new_entry)
                    db.session.flush()  # Get new_entry.id before commit
                    prev.next_id = new_entry.id
                    db.session.commit()
                    return f"Success! Entry with ID {new_entry.id} was added for agent {agent_id}, linked from previous content '{previousContent}' (ID {prev.id})."
                else:
                    return f"Error: Could not find previous content '{previousContent}' in database."
            else:
                # Add new entry and update the last entry's next_id
                new_entry = AgentEntry(agent_id=agent_id, content=content, next_id=None)
                db.session.add(new_entry)
                db.session.flush()  # Get new_entry.id before commit
                last_entry.next_id = new_entry.id
                db.session.commit()
                return f"Success! Entry with ID {new_entry.id} was added for agent {agent_id}, linked from ID {last_entry.id}."
    except Exception as e:
        return f"Error: Could not add entry to database. Details: {e}"



def create_combined_prompt():
    """
    Combines all content in the agent database in linked list order and returns as a single string.
    """
    with app.app_context():
        # Find the head of the linked list (entry not pointed to by any next_id)
        all_ids = {entry.id for entry in AgentEntry.query.all()}
        pointed_ids = {entry.next_id for entry in AgentEntry.query.filter(AgentEntry.next_id != None)}
        head_ids = list(all_ids - pointed_ids)
        if not head_ids:
            return ""
        head_id = min(head_ids)  # If multiple heads, pick the smallest id
        current = AgentEntry.query.get(head_id)
        contents = []
        while current:
            contents.append(current.content)
            if current.next_id is not None:
                current = AgentEntry.query.get(current.next_id)
            else:
                break
        return "\n".join(contents)


def print_all_agent_entries():
    """
    Prints all entries in the agent database in linked list order.
    """
    with app.app_context():
        # Find the head of the linked list (entry not pointed to by any next_id)
        all_ids = {entry.id for entry in AgentEntry.query.all()}
        pointed_ids = {entry.next_id for entry in AgentEntry.query.filter(AgentEntry.next_id != None)}
        head_ids = list(all_ids - pointed_ids)
        if not head_ids:
            print("No entries found in the database.")
            return
        head_id = min(head_ids)  # If multiple heads, pick the smallest id
        current = AgentEntry.query.get(head_id)
        while current:
            print(f"ID: {current.id}, Agent ID: {current.agent_id}, Content: {current.content}, Next ID: {current.next_id}")
            if current.next_id is not None:
                current = AgentEntry.query.get(current.next_id)
            else:
                break

# A helper function to ensure the database is created
def setup_database():
    with app.app_context():
        db.create_all()