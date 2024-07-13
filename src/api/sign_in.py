from flask import Blueprint, request, session, jsonify

from extensions import bcrypt
from db import Personnel

sign_in_bp = Blueprint('sign_in', __name__)
session_bp = Blueprint('session', __name__)

@sign_in_bp.route('/sign-in', methods=['POST'])
def sign_in_api():
	reg_num = request.form.get('reg_num')
	password = request.form.get('password')
	remember = request.form.get('remember_me') == 'on'
	print('Remember:', remember)

	user = Personnel.query.filter_by(reg_num=reg_num).first()

	if user is None:
		return jsonify({'success': False, 'message': 'User not found'}), 404
	elif not bcrypt.check_password_hash(user.password, password):
		return jsonify({'success': False, 'message': 'Incorrect password'}), 401

	session['user'] = user.reg_num
	
	#if remember:
	#	print('\033[92m + Session set to permanent\033[0m')
	#	session.permanent = True
	#else:
	#	print('\033[93m - Session set to non-permanent\033[0m')
	#	session.permanent = False

	print('Session:', session)

	print('\033[92m + User with registration number', user.reg_num, 'signed in successfully\033[0m')
	return jsonify({'success': True, 'message': 'Signed in successfully', 'remember': remember}), 200

@session_bp.route('/re-establish', methods=['POST'])
def reestablish_session():
	data = request.get_json()
	reg_num = data.get('reg_num')

	user = Personnel.query.filter_by(reg_num=reg_num).first()

	if user is None:
		return jsonify({'success': False, 'message': 'User not found'}), 404
	
	session['user'] = user.reg_num
	print('Session:', session)

	print('\033[92m + User with registration number', user.reg_num, 're-established session successfully\033[0m')
	return jsonify({'success': True, 'message': 'Session re-established successfully'}), 200