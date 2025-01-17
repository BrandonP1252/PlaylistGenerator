import os

from dotenv import load_dotenv
from flask import Flask

from .routes import main
from .services import generate_playlist

load_dotenv()

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

#Flask application setup
app = Flask(__name__)
app.register_blueprint(main)
app.secret_key = os.getenv("SECRET_KEY")




