from flask import Blueprint, request, render_template, session
from db import Personnel
import cloudinary
from cloudinary.utils import cloudinary_url
import secrets
from init import bcrypt
from db import db
import hashlib

####### GENERAL ROUTES #######
ping_bp = Blueprint('ping', __name__)
@ping_bp.route('/ping')
def ping():
	print('\033[92m + Pong\033[0m')
	return 'Pong', 200

exit_bp = Blueprint('exit', __name__)
@exit_bp.route('/exit')
def exit():
	session.clear()
	db.session.remove()
	print('\033[93m - Session cleared successfully\033[0m')
	quit()

dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

####### EMPLOYEE ROUTES #######
manage_bp = Blueprint('manage_employees', __name__)
@manage_bp.route('/manage-employees')
def manage_employees():
	employees = Personnel.query.filter_by(deleted=False).all()
	return render_template('manage.html', employees=employees, cloudinary_url=cloudinary_url)

add_bp = Blueprint('add_employee', __name__)
@add_bp.route('/add-employee', methods=['POST', 'GET'])
def add_employee():
	if request.method == 'POST':
		print('\033[94m - POST: Adding employee\033[0m')
		
		cin = request.form.get('cin')
		if Personnel.query.filter_by(cin=cin).first():
			print('\033[91m - Employee with CIN already exists\033[0m')
			return {'success': False, 'message': 'Employee with CIN already exists'}, 400
		
		email = request.form.get('email')
		if Personnel.query.filter_by(email=email).first():
			print('\033[91m - Employee with email already exists\033[0m')
			return {'success': False, 'message': 'Employee with email already exists'}, 400
		
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		function = request.form.get('function')
		phone = request.form.get('phone')
		password = secrets.token_hex(8)

		# Generate a unique registration number based on the CIN
		# This is done by hashing the CIN, then converting it to hexadecimal to get a unique employee number
		# The first 8 characters of the hash are used as the registration number
		reg_num = hashlib.md5(str(cin).encode()).hexdigest()[:8]

		photo = request.files.get('photo')
		if not photo:
			print('\033[91m - No photo provided\033[0m')
			return {'success': False, 'message': 'No photo provided'}, 400

		# Save the image to cloudinary
		res = cloudinary.uploader.upload(photo, public_id = reg_num)
		print('\033[94m + Image uploaded successfully to cloudinary: ', res['url'], '\033[0m')

		# Insert the employee data
		db.session.add(Personnel(
			cin=cin,
			first_name=first_name,
			last_name=last_name,
			reg_num=reg_num,
			dept=function,
			phone=phone,
			email=email,
			password=bcrypt.generate_password_hash(password).decode('utf-8'),
			deleted=False,
			is_admin=False,
			photo=reg_num
		))
		db.session.commit()
		print('\033[94m + Employee added successfully\033[0m')

		return {'success': True, 'message': 'Employee added successfully'}, 200
	else:
		print('\033[94m - GET: Showing add employee form\033[0m')
		return render_template('add.html')

edit_bp = Blueprint('edit_employee', __name__)
@edit_bp.route('/edit-employee/<cin>', methods=['POST', 'GET'])
def edit_employee(cin):
	employee = Personnel.query.filter_by(cin=cin).first()
	if request.method == 'POST':
		print('POST')
		print(f'Editing employee with CIN: {cin}')
		return render_template('edit.html', employee=employee, cloudinary_url=cloudinary_url)
	else:
		print('GET')
		print(f'Showing employee with CIN: {cin}')
		return render_template('edit.html', employee=employee, cloudinary_url=cloudinary_url)

delete_bp = Blueprint('delete_employee', __name__)
@delete_bp.route('/delete-employee/<cin>', methods=['POST', 'GET'])
def delete_employee(cin):
	employee = Personnel.query.filter_by(cin=cin).first()
	if request.method == 'POST':
		print('POST')
		print(f'Deleting employee with CIN: {cin}')
		return render_template('delete.html')
	else:
		print('GET')
		print(f'Showing employee with CIN: {cin}')
		return render_template('delete.html')
	
trash_bp = Blueprint('trash', __name__)
@trash_bp.route('/trash-bin')
def trash():
	employees = Personnel.query.filter_by(deleted=True).all()
	return render_template('trash.html', employees=employees)