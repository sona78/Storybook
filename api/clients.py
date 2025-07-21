from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import openai
import os
from supabase import create_client, Client
from google import genai
load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=os.getenv("OPENAI_API_KEY")
)

llm_client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

google_client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=os.environ.get("GEMINI_API_KEY"),
)
