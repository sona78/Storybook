from clients import llm_client


STYLE = "Pop Art"

def generateRobustPrompt(prompt: str):
    """
    Given a sentence from the story, generate a detailed, vivid, and visually descriptive prompt suitable for an image generation model.
    """
    system_prompt = (
        f"You are an expert at crafting prompts for AI image generation. "
        f"Given a sentence from a story, rewrite it as a detailed, visually rich prompt for an image generator. "
        f"Use the style: {STYLE}. "
        f"Focus on visual elements, mood, setting, and character appearance. "
        f"Do not include text or dialogue in the image. "
        f"Output only the improved prompt."
    )
    completion = llm_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )
    image_prompt = completion.choices[0].message.content
    
    if image_prompt == None or image_prompt.__len__ == 0:
        raise Exception("Failed to generate robust prompt")

    return image_prompt


def generateIllustration(image_prompt: str, story: str):
    try:
        # image_prompt = generateRobustPrompt(prompt)
        image_prompt = f"Given the story so far: {story}, Generate an image for the next sentence of the story given {image_prompt} Generate image using the style of {STYLE}. Do not include text or dialogue in the image."
        print(f"image {image_prompt}")
        response = llm_client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1, # n must be 1 for dall-e-3
        )

        image_url = response.data[0].url
        print(response.data[0].url)
        return response.data[0]

    except Exception as e:
        return f"An OpenAI API error occurred: {e}"
