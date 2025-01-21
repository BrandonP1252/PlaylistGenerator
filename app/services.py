import os
import time
import google.generativeai as genai
import json
import spotipy
from dotenv import load_dotenv
from flask import redirect, url_for

from .auth import get_token
from .schemas import Song

load_dotenv()

# Creates a list of songs based on the parameters given
def generate_playlist(music_list, number_of_songs):
    time.sleep(5)
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


def get_user_playlists():
    try:
        token_info = get_token()
    except():
        print("User is not logged in")
        return redirect(url_for("main.login"))

    sp = spotipy.Spotify(auth=token_info["access_token"])
    playlists = sp.current_user_playlists()["items"]
    names = []
    for playlist in playlists:
        names.append(playlist["name"])
    return names

# Converts list of songs into a list of uris
def get_uri_list():
    try:
        token_info = get_token()
    except():
        print("User is not logged in")
        return redirect(url_for("main.login"))

    sp = spotipy.Spotify(auth=token_info["access_token"])
    playlist_generated_names = generate_playlist(["Bad Bunny"], 20)

    uri_list = []
    for song in playlist_generated_names:
        song_name = song["song_name"] + " " + song["artist_name"]
        song_search = sp.search(q=song_name, type='track', limit=1, market=None)
        uri_list.append(song_search["tracks"]["items"][0]["uri"])

    return uri_list

# Creates a playlist and adds it to your Spotify account
def create_playlist(name):
    try:
        token_info = get_token()
    except():
        print("User is not logged in")
        return redirect(url_for("main.login"))

    sp = spotipy.Spotify(auth=token_info["access_token"])
    playlist = sp.user_playlist_create(get_user_id(), name, public=False, collaborative=False)
    return playlist["id"]

# Returns the id of the user
def get_user_id():
    try:
        token_info = get_token()
    except():
        print("User is not logged in")
        return redirect(url_for("main.login"))

    sp = spotipy.Spotify(auth=token_info["access_token"])
    return sp.current_user()["id"]

def add_songs_to_playlist(playlist_id, uri_list):
    try:
        token_info = get_token()
    except():
        print("User is not logged in")
        return redirect(url_for("main.login"))

    sp = spotipy.Spotify(auth=token_info["access_token"])
    sp.playlist_add_items(playlist_id, uri_list, position=None)
    return playlist_id