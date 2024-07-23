from flask import Blueprint, request, session, jsonify, render_template

from init import bcrypt
from db import Personnel

sign_in_bp = Blueprint('sign_in', __name__)

@sign_in_bp.route('/sign-in', methods=['GET', 'POST'])
def sign_in_api():
	if request.method == 'POST':
		print('POST: Sign in')
		
		reg_num = request.json.get('reg_num')
		password = request.json.get('password')
		remember = request.json.get('remember_me') == 'on'
		print('Remember:', remember)

		user = Personnel.query.filter_by(reg_num=reg_num).first()

		if user is None:
			return jsonify({'success': False, 'message': 'User not found'}), 404
		elif not bcrypt.check_password_hash(user.password, password):
			return jsonify({'success': False, 'message': 'Incorrect password'}), 401

		session['user'] = user.reg_num
		
		if remember:
			print('\033[92m + Session set to permanent\033[0m')
			session.permanent = True
		else:
			print('\033[93m - Session set to non-permanent\033[0m')
			session.permanent = False

		print('\033[92m + User with registration number', user.reg_num, 'signed in successfully\033[0m')
		return jsonify({'success': True, 'message': 'Signed in successfully', 'user': user.reg_num}), 200
	else:
		print('GET: Sign in')
		return render_template('index.html')

@sign_in_bp.route('/validate-session', methods=['POST'])
def validate_session():
	reg_num = request.json.get('user')

	# Check if the user exists in the database
	user = Personnel.query.filter_by(reg_num=reg_num).first()
	if user is None:
		print('\033[91m - User', reg_num, 'not found\033[0m')
		return jsonify({'success': False, 'message': 'User not found'}), 404

	session['user'] = reg_num
	print('\033[92m + Session validated successfully\033[0m')
	return jsonify({'success': True, 'message': 'Session validated successfully', 'user': reg_num}), 200


import face_recognition
from cloudinary.utils import cloudinary_url
from urllib.request import urlopen

@sign_in_bp.route('/face-recognition', methods=['POST'])
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
			return jsonify({'success': False, 'error': 'No face detected'})
		print('\033[92m + Face detected successfully\033[0m')

		# Compare face encoding with known face encodings from the database
		for face_encoding in face_encodings:
			personnel = Personnel.query.filter_by(deleted=False).all()

			for person in personnel:
				person_image_url = cloudinary_url(person.photo)[0]
				known_image = face_recognition.load_image_file(urlopen(person_image_url))
				known_face_encoding = face_recognition.face_encodings(known_image)[0]
				results = face_recognition.compare_faces([known_face_encoding], face_encoding)

				if results[0]:
					return jsonify({
						'success': True,
						'cin': person.cin,
						'first_name': person.first_name,
						'last_name': person.last_name,
						'reg_num': person.reg_num,
						'dept': person.dept,
						'phone': person.phone,
						'email': person.email
					})
				
		return jsonify({'success': False, 'error': 'Face not recognized'})