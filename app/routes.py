from flask import Blueprint, session, redirect, request, url_for

from .auth import get_token, create_spotify_oauth

main = Blueprint('main', __name__)

@main.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@main.route('/callback')
def callback():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("main.test"))

@main.route('/test')
def test():
    return session.get("token_info", None)
