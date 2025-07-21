from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from prompt_of_the_day import getPromptOfTheDay
from image import generateIllustration
from db import add_agent_entry, create_combined_prompt
from clients import llm
from datetime import datetime, timezone
from storage import uploadFile

template = """
You are collaboratively building a story, one step at a time.
Here is the story so far:
{story_so_far}

A user now suggests: "{new_user_prompt}"

Continue the story with a single sentence, reflecting this new prompt and the story's context, and without giving an ending.
"""

prompt_template = PromptTemplate(
    input_variables=["story_so_far", "new_user_prompt"],
    template=template
)

@tool
def add_to_story(new_user_prompt: str):
    """Add to the collaborative story using the latest user prompt."""

    current_datetime = datetime.now(timezone.utc)

    story_so_far = create_combined_prompt()
    if not story_so_far:
        # If the story is empty, use the prompt of the day as the initial theme
        potd = getPromptOfTheDay(current_datetime)
        if potd:
            story_so_far = f"[Theme: {potd['prompt']}]"
    prompt = prompt_template.format(
        story_so_far=story_so_far,
        new_user_prompt=new_user_prompt
    )
    response = llm.invoke(prompt)
    content = response.content

    image = generateIllustration(str(content), story_so_far)
    print(image)
    image_prompt = image.revised_prompt
    image_url = uploadFile(image.url, image_prompt, current_datetime)

    add_agent_entry(content, image_prompt, image_url, current_datetime)
    return content