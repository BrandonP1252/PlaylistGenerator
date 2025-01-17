import os
import time
from flask import Flask, redirect, url_for, session, request
from dotenv import load_dotenv
from spotipy import SpotifyOAuth

load_dotenv()


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-library-read playlist-modify-public playlist-modify-private playlist-read-private user-read-private"
    )

# Checks if token is expired and refreshes it
def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect(url_for("main.login"))
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        spotify_auth = create_spotify_oauth()
        token_info = spotify_auth.refresh_access_token(token_info["refresh_token"])
    return token_info