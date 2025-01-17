from flask import Blueprint, session, redirect, request, url_for

from .auth import get_token, create_spotify_oauth
from .services import get_user_playlists, get_uri_list, create_playlist, get_user_id

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
    return redirect(url_for("main.user_playlists"))

@main.route('/uri-list')
def uri_list():
    return get_uri_list()

@main.route('/create-playlist')
def create_user_playlist():
    return create_playlist()

@main.route('/get-user-id')
def user_id():
    return get_user_id()

@main.route('/get-user-playlists')
def user_playlists():
    return get_user_playlists()