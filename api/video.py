import time
import os
from google import genai
from google.genai import types
from clients import google_client

MODEL = "veo-2.0-generate-001"


video_config = types.GenerateVideosConfig(
    person_generation="dont_allow", # supported values: "dont_allow" or "allow_adult" or "allow_all"
    aspect_ratio="16:9", # supported values: "16:9" or "16:10"
    number_of_videos=1, # supported values: 1 - 4
    duration_seconds=8, # supported values: 5 - 8
)

def generateVideo(story: str):
    operation = google_client.models.generate_videos(
        model=MODEL,
        prompt=story,
        config=video_config,
    )

    # Waiting for the video(s) to be generated
    while not operation.done:
        print("Video has not been generated yet. Check again in 10 seconds...")
        time.sleep(10)
        operation = google_client.operations.get(operation)

    result = operation.result
    if not result:
        print("Error occurred while generating video.")
        return

    generated_videos = result.generated_videos
    if not generated_videos:
        print("No videos were generated.")
        return

    print(f"Generated {len(generated_videos)} video(s).")
    for n, generated_video in enumerate(generated_videos):
        print(f"Video has been generated: {generated_video.video.uri}")
        google_client.files.download(file=generated_video.video)
        generated_video.video.save(f"video_{n}.mp4") # Saves the video(s)
        print(f"Video {generated_video.video.uri} has been downloaded to video_{n}.mp4.")
