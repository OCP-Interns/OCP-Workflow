from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import timedelta
import os

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=7)
app.secret_key = os.getenv('SECRET_KEY')

#app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
#app.config['SESSION_COOKIE_SECURE'] = False

cors = CORS()
bcrypt = Bcrypt()