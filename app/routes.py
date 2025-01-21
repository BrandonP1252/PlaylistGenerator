from flask import Blueprint, session, redirect, request, url_for

from .auth import create_spotify_oauth
from .services import get_user_playlists, get_uri_list, create_playlist, get_user_id, add_songs_to_playlist

main = Blueprint('main', __name__)

# Signs in to Spotify
@main.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

# Callback redirect from Spotify
@main.route('/callback')
def callback():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("main.uri_list"))

@main.route('/uri-list')
def uri_list():
    return get_uri_list()

@main.route('/create-playlist/<name>')
def create_user_playlist(name):
    return create_playlist(name)

@main.route('/get-user-id')
def user_id():
    return get_user_id()

@main.route('/get-user-playlists')
def user_playlists():
    return get_user_playlists()

@main.route('/song_playlist')
def song_playlist():
    return add_songs_to_playlist(create_playlist("test playlist"), get_uri_list())