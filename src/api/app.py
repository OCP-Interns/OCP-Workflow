from flask import Flask, request, jsonify, render_template
import face_recognition
import numpy as np
import json

from db import init_db
from sign_in import sign_in_bp, session_bp
from extensions import *
from db import Personnel

def create_app():	
	cors.init_app(app)
	bcrypt.init_app(app)
	db = init_db(app)

	app.register_blueprint(sign_in_bp)
	app.register_blueprint(session_bp)
	
	return app, db

app, db = create_app()

@app.route('/face-recognition', methods=['POST'])
def face_recognition_api():
	if 'file' not in request.files:
		return jsonify({'error': 'No file part'})
	
	file = request.files['file']

	if file.filename == '':
		return jsonify({'error': 'No selected file'})
	
	print('File:', file.filename)
	print('\033[92m + File received successfully\033[0m')
	
	if file:
		image = face_recognition.load_image_file(file)
		face_locations = face_recognition.face_locations(image)
		face_encodings = face_recognition.face_encodings(image, face_locations)

		print('Number of faces:', len(face_encodings))
		if len(face_encodings) == 0:
			return jsonify({'error': 'No face detected'})
		print('\033[92m + Face detected successfully\033[0m')

		# Compare face encoding with known face encodings from the database
		for face_encoding in face_encodings:
			personnel = Personnel.query.filter_by(deleted=False).all()

			for person in personnel:
				known_face_encoding = np.array(json.loads(person.face_encoding))
				results = face_recognition.compare_faces([known_face_encoding], face_encoding)

				if results[0]:
					return jsonify({
						'cin': person.cin,
						'first_name': person.first_name,
						'last_name': person.last_name,
						'reg_num': person.reg_num,
						'dept': person.dept,
						'phone': person.phone,
						'email': person.email
					})
				
		return jsonify({'error': 'No match found'})

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