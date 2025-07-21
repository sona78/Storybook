from datetime import datetime
from clients import supabase
import requests
import os
import io
from PIL import Image
import hashlib
import uuid


BUCKET_NAME = 'illustrations'


def uploadFile(image_url: str, image_prompt: str, datetime: datetime):
    try:
        # Step 1: Fetch the image into an in-memory stream
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Step 2: Open, convert, and save to a new in-memory buffer (io.BytesIO)
        # No files are touched on the local disk.
        with Image.open(io.BytesIO(response.content)) as img:
            rgb_img = img.convert("RGB")
            output_buffer = io.BytesIO()
            rgb_img.save(output_buffer, format="JPEG", quality=90)
            output_buffer.seek(0) # Rewind buffer to the beginning

            # Step 3: Define the destination path in Supabase
            supabase_path = f"{datetime.date()}/{uuid.uuid4()}"

            # Step 4: Upload the in-memory buffer directly to Supabase
            print(f"Streaming to Supabase bucket '{BUCKET_NAME}'...")
            supabase.storage.from_(BUCKET_NAME).upload(
                path=supabase_path,
                file=output_buffer.getvalue(), # Uploading from the in-memory buffer
                file_options={"content-type": "image/jpeg", "upsert": "true"}
            )
            print("Stream and upload complete.")

            # 2. Create a signed URL for the uploaded file
            url_response = supabase.storage.from_(BUCKET_NAME).get_public_url(
                path=supabase_path
            )
            
            return url_response

    except Exception as e:
        print(f"An error occurred during the stream process: {e}")

    