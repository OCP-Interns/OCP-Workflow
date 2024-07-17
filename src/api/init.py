from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import timedelta
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.permanent_session_lifetime = timedelta(days=7)
app.secret_key = os.getenv('SECRET_KEY')

cors = CORS()
bcrypt = Bcrypt()