from mcp import add_to_story
from db import create_combined_prompt, add_agent_entry
from prompt_of_the_day import getPromptOfTheDay
from image import generateIllustration, generateRobustPrompt

if __name__ == "__main__":
    # set_prompt_of_the_day("SF Tech Lore")
    # print(get_prompt_of_the_day())
    # print_all_agent_entries()
    # print(generateRobustPrompt("Rumors began to circulate about the stranger's past, with some claiming they were a fugitive on the run and others believing them to be a lost noble searching for something precious."))
    # add_agent_entry("test", "test1", "test2")
    # print(create_combined_prompt())
    # print_all_agent_entries()
    getPromptOfTheDay()
    # add_to_story()
    