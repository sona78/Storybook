from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=os.getenv("OPENAI_API_KEY")
)