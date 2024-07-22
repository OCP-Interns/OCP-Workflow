import face_recognition
import json
from flask import render_template

from db import init_db
from sign_in import sign_in_bp, session_bp, face_recognition_bp
from routes import ping_bp, dashboard_bp, manage_bp, add_bp, edit_bp, delete_bp, trash_bp, AddTableTime_bp, time_view_bp
from init import *

def create_app():	
	cors.init_app(app)
	bcrypt.init_app(app)
	db = init_db(app)

	app.register_blueprint(ping_bp)
	app.register_blueprint(sign_in_bp)
	app.register_blueprint(session_bp)
	app.register_blueprint(face_recognition_bp)
	app.register_blueprint(dashboard_bp)
	app.register_blueprint(manage_bp)
	app.register_blueprint(add_bp)
	app.register_blueprint(edit_bp)
	app.register_blueprint(delete_bp)
	app.register_blueprint(trash_bp)
	app.register_blueprint(AddTableTime_bp)
	app.register_blueprint(time_view_bp)
	
	return app, db

app, db = create_app()

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

from db import Personnel
from cloudinary.utils import cloudinary_url
from urllib.request import urlopen

# Insert the default personnel data
with app.app_context():
	if not Personnel.query.first():
		# Load image from cloudinary
		image_url = cloudinary_url('i_me')[0]
		image_of_default_person = face_recognition.load_image_file(urlopen(image_url))
		face_encodings = face_recognition.face_encodings(image_of_default_person)

		if not face_encodings:
			raise Exception('No face detected in the image')
		
		default_person_face_encoding = face_encodings[0]
		db.session.add(Personnel(
			cin='HH123456',
			first_name='Someone',
			last_name='Guy',
			reg_num='IT123456',
			dept='IT',
			phone='123456',
			email='someguy@gmail.com',
			password=bcrypt.generate_password_hash('123456').decode('utf-8'),
			deleted=False,
			is_admin=True,
			photo='i_me'
		))
		db.session.commit()
		print('\033[92m + Default user inserted successfully\033[0m')
	else:
		print('\033[94m - Default user already exists\033[0m')

if __name__ == '__main__':
	app.run(debug=True)