import os
from langchain_openai import ChatOpenAI
from db import add_agent_entry, setup_database  # Use db.py, not mcp
from llm import llm

# Ensure the database file and table exist before running
print("Setting up database...")
setup_database()

# --- Agent Creation ---
# 1. Choose the LLM model that will be the "brain" of the agent

# 2. Define the list of tools the agent can use
tools = [add_agent_entry]

# 3. Bind the tools to the LLM
# This tells the model that it has these actions available
llm_with_tools = llm.bind_tools(tools)

# --- Running the Agent ---
# This is the high-level task for the agent.
# Notice it's just natural language.
prompt = "Hello, I am agent-alpha and I'd like to add a creative prompt to the overall prompt block"

print(f"\nInvoking agent with prompt: '{prompt}'")

# The agent's brain (the LLM) processes the prompt and the available tools.
# It recognizes that "make a note" matches the purpose of the `add_agent_entry` tool.
response = llm_with_tools.invoke(prompt)

print("\n--- Agent Response ---")
print(f"Content: {response.content}")

# Try to access tool_calls if present (for OpenAI tool calling, it's usually in response.additional_kwargs)
tool_calls = getattr(response, "tool_calls", None)
if tool_calls is None:
    tool_calls = response.additional_kwargs.get("tool_calls") if hasattr(response, "additional_kwargs") else None

print(f"Tool Calls: {tool_calls}")

# In a real application, you would now execute the tool call the agent decided on.
# LangChain agent executors do this automatically, but here we do it manually for clarity.
if tool_calls:
    tool_call = tool_calls[0]
    tool_name = tool_call['name']
    tool_args = tool_call['args']

    print(f"\nAgent decided to use the '{tool_name}' tool.")
    print(f"Arguments: {tool_args}")

    # Execute the function with the arguments provided by the LLM
    # The add_agent_entry tool expects keyword arguments
    result = add_agent_entry.invoke(tool_args)
    print(f"\nTool execution result: {result}")