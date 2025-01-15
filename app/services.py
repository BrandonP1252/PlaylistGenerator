import os
import time

import google.generativeai as genai
import json

from dotenv import load_dotenv
from .schemas import Song

load_dotenv()

def generate_playlist(music_list, number_of_songs):
    time.sleep(15)
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"List {number_of_songs} songs related to these genres or artists: {music_list}",
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=list[Song]
        )
    )
    result_data = json.loads(response.text)
    return result_data

