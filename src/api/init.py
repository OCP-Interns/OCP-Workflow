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

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

cloudinary.config(
	cloud_name = os.getenv('CLOUD_NAME'),
	api_key = os.getenv('API_KEY'),
	api_secret = os.getenv('API_SECRET'),
	secure = True
)

#res = cloudinary.uploader.upload("static/images/i_me.png", public_id = "i_me")
#print('\033[92m +', cloudinary_url(res['public_id']), '\033[0m')