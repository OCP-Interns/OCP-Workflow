import face_recognition
import json

from db import init_db
from sign_in import sign_in_bp, session_bp, face_recognition_bp
from extensions import *
from db import Personnel

def create_app():	
	cors.init_app(app)
	bcrypt.init_app(app)
	db = init_db(app)

	app.register_blueprint(sign_in_bp)
	app.register_blueprint(session_bp)
	app.register_blueprint(face_recognition_bp)
	
	return app, db

app, db = create_app()

# Insert the default personnel data
with app.app_context():
	if not Personnel.query.first():
		image_of_default_person = face_recognition.load_image_file("../../assets/i_me.png")
		face_encodings = face_recognition.face_encodings(image_of_default_person)

		if not face_encodings:
			raise Exception('No face detected in the image')
		
		default_person_face_encoding = face_encodings[0]
		db.session.add(Personnel(
			cin='HH123456',
			first_name='Someone',
			last_name='Guy',
			reg_num='123456',
			dept='IT',
			phone='123456',
			email='someguy@gmail.com',
			password=bcrypt.generate_password_hash('123456').decode('utf-8'),
			deleted=False,
			face_encoding=json.dumps(default_person_face_encoding.tolist())
		))
		db.session.commit()
		print('\033[92m + Default user inserted successfully\033[0m')
	else:
		print('\033[94m - Default user already exists\033[0m')

if __name__ == '__main__':
	app.run(debug=True)