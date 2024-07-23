from flask import Blueprint, request, render_template, session
from db import Personnel
import cloudinary
from cloudinary.utils import cloudinary_url
import secrets
from init import bcrypt
from db import db
import hashlib

def generate_8_digit_hash(value):
	return hashlib.md5(str(value).encode()).hexdigest()[:8]

####### GENERAL ROUTES #######
# Combine all the general routes into a single blueprint
general_bp = Blueprint('general_routes', __name__)
@general_bp.route('/ping')
def ping():
	print('\033[92m + Pong\033[0m')
	return 'Pong', 200

@general_bp.route('/exit')
def exit():
	session.clear()
	db.session.remove()
	print('\033[93m - Session cleared successfully\033[0m')
	quit()

@general_bp.route('/dashboard')
def dashboard():
	total_employees = Personnel.query.filter_by(deleted=False).count()

	return render_template('dashboard.html', total_employees= total_employees)

####### EMPLOYEE ROUTES #######
# Combine all the employee routes into a single blueprint
employee_bp = Blueprint('employee_routes', __name__)

@employee_bp.route('/manage-employees')
def manage_employees():
	employees = Personnel.query.filter_by(deleted=False).all()
	return render_template('manage.html', employees=employees, cloudinary_url=cloudinary_url)

@employee_bp.route('/add-employee', methods=['POST', 'GET'])
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
		phone = request.form.get('phone')
		password = secrets.token_hex(8)
		shift = request.form.get('shift')

		# Generate a unique registration number based on the CIN
		# This is done by hashing the CIN, then converting it to hexadecimal to get a unique employee number
		# The first 8 characters of the hash are used as the registration number
		reg_num = generate_8_digit_hash(cin)

		photo = request.files.get('photo')
		if not photo:
			print('\033[91m - No photo provided\033[0m')
			return {'success': False, 'message': 'No photo provided'}, 400

		# Generate a unique ID for the photo to avoid conflicts
		# Cloudinary keeps cached versions of images, which may cause the image not to update
		# The photo ID should be unique and independent of the employee number
		photo_id = generate_8_digit_hash(secrets.token_hex(8))

		# Save the image to cloudinary
		res = cloudinary.uploader.upload(photo, public_id = photo_id)
		print('\033[94m + Image uploaded successfully to cloudinary: ', res['url'], '\033[0m')

		# Insert the employee data
		db.session.add(Personnel(
			reg_num=reg_num,
			cin=cin,
			photo=photo_id,

			first_name=first_name,
			last_name=last_name,
			phone=phone,
			email=email,
			password=bcrypt.generate_password_hash(password).decode('utf-8'),
			shift=shift,

			deleted=False,
			is_admin=False
		))
		try:
			db.session.commit()
			print('\033[94m + Employee added successfully\033[0m')
			return {'success': True, 'message': 'Employee added successfully'}, 200
		except Exception as e:
			print('\033[91m - Error adding employee: ', e, '\033[0m')
			return {'success': False, 'message': 'Error adding employee'}, 500
	else:
		print('\033[94m - GET: Showing add employee form\033[0m')
		return render_template('add.html')

@employee_bp.route('/edit-employee/<cin>', methods=['POST', 'GET'])
def edit_employee(cin):
	employee = Personnel.query.filter_by(cin=cin).first()
	if request.method == 'POST':
		print('\033[94m - POST: Editing employee\033[0m')

		# Check if the CIN has been changed
		new_cin = request.form.get('cin')
		if new_cin != cin and Personnel.query.filter_by(cin=new_cin).first():
			print('\033[91m - Employee with CIN already exists\033[0m')
			return {'success': False, 'message': 'Employee with CIN already exists'}, 400
		
		email = employee.email
		new_email = request.form.get('email')
		if new_email != email and Personnel.query.filter_by(email=new_email).first():
			print('\033[91m - Employee with email already exists\033[0m')
			return {'success': False, 'message': 'Employee with email already exists'}, 400
		
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		phone = request.form.get('phone')
		shift = request.form.get('shift')

		photo = request.files.get('photo')
		if photo:
			# Generate a unique ID for the photo to avoid conflicts
			# Cloudinary keeps cached versions of images, which may cause the image not to update
			# The photo ID should be unique and independent of the employee number
			photo_id = generate_8_digit_hash(secrets.token_hex(8))

			# Save the image to cloudinary
			res = cloudinary.uploader.upload(photo, public_id = photo_id)
			print('\033[94m + Image uploaded successfully to cloudinary: ', res['url'], '\033[0m')

			employee.photo = photo_id

		employee.cin = new_cin
		employee.first_name = first_name
		employee.last_name = last_name
		employee.phone = phone
		employee.email = email
		employee.shift = shift

		try:
			db.session.commit()
			print('\033[94m + Employee edited successfully\033[0m')
			return {'success': True, 'message': 'Employee edited successfully'}, 200
		except Exception as e:
			print('\033[91m - Error editing employee: ', e, '\033[0m')
			return {'success': False, 'message': 'Error editing employee'}, 500
	else:
		print('\033[94m - GET: Showing edit employee form\033[0m')
		return render_template('edit.html', employee=employee, cloudinary_url=cloudinary_url)

@employee_bp.route('/delete-employee/<cin>', methods=['POST'])
def delete_employee(cin):
	employee = Personnel.query.filter_by(cin=cin).first()
	employee.deleted = True
	try:
		db.session.commit()
		print('\033[94m + Employee deleted successfully\033[0m')
		return {'success': True, 'message': 'Employee deleted successfully'}, 200
	except Exception as e:
		print('\033[91m - Error deleting employee: ', e, '\033[0m')
		return {'success': False, 'message': 'Error deleting employee'}, 500
	
@employee_bp.route('/restore-employee/<cin>', methods=['POST'])
def restore_employee(cin):
	employee = Personnel.query.filter_by(cin=cin).first()
	employee.deleted = False
	try:
		db.session.commit()
		print('\033[94m + Employee restored successfully\033[0m')
		return {'success': True, 'message': 'Employee restored successfully'}, 200
	except Exception as e:
		print('\033[91m - Error restoring employee: ', e, '\033[0m')
		return {'success': False, 'message': 'Error restoring employee'}, 500

@employee_bp.route('/trash-bin')
def trash():
	employees = Personnel.query.filter_by(deleted=True).all()
	return render_template('trash.html', employees=employees, cloudinary_url=cloudinary_url)


schedule = {day: {f'{hour:02}:00 - {hour + 1:02}:00': [] for hour in range(23)} for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
for day in schedule:
    schedule[day]['23:00 - 00:00'] = []

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET', 'POST'])
def events():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours = [f'{hour:02}:00 - {hour + 1:02}:00' for hour in range(23)] + ['23:00 - 00:00']
    employees = Personnel.query.filter_by(deleted=False).all()
    
    if request.method == 'POST':
        day = request.form['day']
        start_hour = request.form['start_hour']
        end_hour = request.form['end_hour']
        event = request.form['event']
        event_emp = request.form['event_emp']  # Get the selected employee
        
        start_index = hours.index(start_hour)
        end_index = hours.index(end_hour)
        
        if start_index <= end_index:
            for hour in hours[start_index:end_index + 1]:
                schedule[day][hour].append((event, event_emp))
        else:
            for hour in hours[start_index:]:
                schedule[day][hour].append((event, event_emp))
            next_day = days[(days.index(day) + 1) % 7]
            for hour in hours[:end_index + 1]:
                schedule[next_day][hour].append((event, event_emp))
    
    return render_template('event.html', days=days, hours=hours, schedule=schedule, employees=employees)
