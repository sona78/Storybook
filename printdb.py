from db import print_all_agent_entries
from prompt_of_the_day import set_prompt_of_the_day

if __name__ == "__main__":
    set_prompt_of_the_day("SF Tech Lore")
    print_all_agent_entries()