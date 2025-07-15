from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from db import add_agent_entry, create_combined_prompt
from llm import llm
from prompt_of_the_day import get_prompt_of_the_day

template = """
You are collaboratively building a story, one step at a time.
Here is the story so far:
{story_so_far}

A user now suggests: "{new_user_prompt}"

Continue the story with a single sentence, reflecting this new prompt, and without giving an ending.
"""

prompt_template = PromptTemplate(
    input_variables=["story_so_far", "new_user_prompt"],
    template=template
)

@tool
def add_to_story(new_user_prompt: str) -> str:
    """Add to the collaborative story using the latest user prompt."""
    story_so_far = create_combined_prompt()
    if not story_so_far:
        # If the story is empty, use the prompt of the day as the initial theme
        potd = get_prompt_of_the_day()
        if potd:
            story_so_far = f"[Theme: {potd}]"
    prompt = prompt_template.format(
        story_so_far=story_so_far,
        new_user_prompt=new_user_prompt
    )
    response = llm.invoke(prompt)
    content = response.content
    if isinstance(content, list):
        next_fragment = " ".join(str(x) for x in content).strip()
    else:
        next_fragment = str(content).strip()
    add_agent_entry(next_fragment)
    return next_fragment