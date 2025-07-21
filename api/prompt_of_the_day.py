from datetime import datetime
from clients import supabase, llm_client

STORYBOOK_PROMPTS = "storybook_daily_prompts"

def generateTitle() -> str:
    system_prompt = (
        "You are a creative assistant for children's books. "
        "Given a story prompt, generate a catchy, imaginative, and age-appropriate book title in a few words (no more than 8). "
        "The title should be fun, engaging, and suitable for children ages 5-15. "
        "Do not include subtitles or explanations, just the title."
    )

    # For demonstration, let's use a placeholder prompt; in practice, pass the actual prompt as an argument
    example_prompt = "A group of adventurous kittens build a rocket to visit the moon."

    completion = llm_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Prompt: {example_prompt}\nGenerate a book title:"}
        ],
        temperature=0.9,
        max_tokens=12
    )
    title = completion.choices[0].message.content.strip()
    if not title:
        raise Exception("Failed to generate a title.")
    return title


def generatePrompt() -> str:
    system_prompt = (
        "You are a creative assistant for children's stories. "
        "Generate a unique, imaginative, and engaging prompt for a children's storybook. "
        "The prompt should inspire a fun, adventurous, or heartwarming story suitable for children ages 5-15. "
        "Keep it concise (1-2 sentences), and do not include any inappropriate or scary content."
    )

    completion = llm_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Please generate a random prompt for a children's storybook."}
        ],
        temperature=1,
        max_tokens=60
    )
    prompt = completion.choices[0].message.content.strip()
    if not prompt:
        raise Exception("Failed to generate a prompt of the day.")
    return prompt

def getPromptOfTheDay(datetime: datetime):
    try:

        today = datetime.date().isoformat()
        entries = (
            supabase.table(STORYBOOK_PROMPTS)
            .select("*")
            .eq("date", today)
            .execute()
        ).data


        if len(entries) > 0:
            return entries[0]
        


        prompt = generatePrompt()
        title = generateTitle()
        story_data = {
            "date": today,
            "prompt": prompt,
            "title": title
        }
        # Select the table and insert the data
        supabase.table(STORYBOOK_PROMPTS).insert(story_data).execute()
        
        return story_data
            
        # story_data = {
        #     "content": content,
        #     "datetime": datetime.isoformat(),
        #     "image_prompt": image_prompt,
        #     "image_url": image_url
        # }
        #     # Select the table and insert the data
        # data, count = supabase.table('storybook').insert(story_data).execute()
        

        #             entries = (
        #         supabase.table("storybook")
        #         .select("*")
        #         .execute()
        #     ).data
    except Exception as e:
        print(e)