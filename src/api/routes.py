from flask import Blueprint, redirect, request, jsonify, render_template, session, url_for
from db import Personnel, Event, TimeTable, db
import cloudinary
from cloudinary.utils import cloudinary_url
import secrets
from init import bcrypt
import json
import hashlib
import os
import qrcode
from datetime import datetime



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
	total_managers = Personnel.query.filter_by(is_admin=1).count()
	total_Meetings = Event.query.count()
	return render_template('dashboard.html', total_employees= total_employees,total_Meetings=total_Meetings,total_managers=total_managers, page='dashboard')

####### EMPLOYEE ROUTES #######
# Combine all the employee routes into a single blueprint
employee_bp = Blueprint('employee_routes', __name__)

## EMPLOYEES ##
@employee_bp.route('/manage-employees')
def manage_employees():
	employees = Personnel.query.filter_by(deleted=False).all()
	return render_template('manage.html', employees=employees, cloudinary_url=cloudinary_url, page='employees')

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
		return render_template('add.html', page='employees')

@employee_bp.route('/edit-employee-details/<cin>', methods=['POST', 'GET'])
def edit_employee_details(cin):
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
		return render_template('edit.html', employee=employee, cloudinary_url=cloudinary_url, page='employees')

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
	return render_template('trash.html', employees=employees, cloudinary_url=cloudinary_url, page='trash')
@employee_bp.route('/permanent-delete-employee/<cin>', methods=['POST'])
def permanent_delete_employee(cin):
    employee = Personnel.query.filter_by(cin=cin).first()
    if employee:
        try:
            # Manually delete related timetable entries
            TimeTable.query.filter_by(personnel_reg_num=employee.reg_num).delete()

            # Now delete the employee
            db.session.delete(employee)
            db.session.commit()
            print('\033[94m + Employee permanently deleted successfully\033[0m')
            return {'success': True, 'message': 'Employee permanently deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print('\033[91m - Error permanently deleting employee: ', e, '\033[0m')
            return {'success': False, 'message': 'Error permanently deleting employee'}, 500
    else:
        return {'success': False, 'message': 'Employee not found'}, 404


## TIMETABLE ##
@employee_bp.route('/edit-employee-timetable/<personnel_reg_num>', methods=['GET', 'POST'])
def edit_employee_timetable(personnel_reg_num):
	employee = Personnel.query.filter_by(reg_num=personnel_reg_num).first()
	if request.method == 'POST':
		timetable_json = request.form.get('timetable_json')
		if timetable_json:
			timetable_data = json.loads(timetable_json)
			#* HERE
			# Check if the employee already has a timetable
			existing_employee = TimeTable.query.filter_by(personnel_reg_num=personnel_reg_num).first()
			# Load the existing timetable data if it exists
			existing_timetable = json.loads(existing_employee.json) if existing_employee else {}
			# Add the new time to the timetable
			add_time(timetable_data, existing_timetable, personnel_reg_num)

			#?{
			#new_entry = TimeTable(personnel_reg_num=personnel_reg_num, json=timetable_data)
			#db.session.add(new_entry)
			#db.session.commit()
			#?}
			return jsonify({'success': True, 'message': 'Timetable updated successfully'}), 200
		else:
			return jsonify({'success': False, 'message': 'No timetable data provided'}), 400
	else:
		return render_template('timetable.html', employee=employee, cloudinary_url=cloudinary_url, page='employees')

#* HERE
# This function converts a time interval to a list of integers for easier comparison
def to_interval(timetable_data):
	# Convert the time to integers for easier comparison (e.g. "08:00" -> 8)
	from_time = int(timetable_data["from"].split(":")[0])
	to_time = int(timetable_data["to"].split(":")[0])
	return [from_time, to_time]
# This function converts a time string to a datetime object
def to_datetime(time_str):
    return datetime.strptime(time_str, '%H:%M')
# This function adds a time interval to the timetable
def add_time(timetable_data, timetable, reg_num):
	day = timetable_data["day"]
	interval = {"from": timetable_data["from"], "to": timetable_data["to"]}
	interval_int = to_interval(timetable_data)
	# Check if the day is already in the timetable
	if day in timetable:
		overlapping_intervals = []
		# Check if the interval is already in the timetable
		for existing_interval in timetable[day]:
			# Convert the existing interval to integers for easier comparison
			existing_interval_int = to_interval(existing_interval)

			# Check if the intervals overlap
			if (interval_int[0] >= existing_interval_int[0] and interval_int[0] <= existing_interval_int[1]) or \
			   (interval_int[1] >= existing_interval_int[0] and interval_int[1] <= existing_interval_int[1]):
				
				overlapping_intervals.append(existing_interval)
				# The intervals overlap, merge them and convert them back to strings
				interval['from'] = min(interval['from'], existing_interval['from'], key=to_datetime)
				interval['to'] = max(interval['to'], existing_interval['to'], key=to_datetime)
				# To compare with other intervals, we replace the interval to insert with the merged interval
				interval_int = to_interval(interval)
				
		# Remove the overlapping intervals from the timetable
		for existing_interval in overlapping_intervals:
			timetable[day].remove(existing_interval)
		# Add the merged interval to the timetable
		timetable[day].append(interval)
	# If the day is not in the timetable then add it
	else:
		# Add the day and interval to the timetable
		timetable[day] = [interval]
	
	employee = TimeTable.query.filter_by(personnel_reg_num=reg_num).first()
	if employee:
		employee.json = json.dumps(timetable)
	else:
		new_entry = TimeTable(personnel_reg_num=reg_num, json=json.dumps(timetable))
		db.session.add(new_entry)
	db.session.commit()

@employee_bp.route('/edit-employee-timetable/json/<personnel_reg_num>', methods=['GET'])
def employee_timetable(personnel_reg_num):
	timetable = TimeTable.query.filter_by(personnel_reg_num=personnel_reg_num).all()
	print(f"Requested timetable for personnel_reg_num: {personnel_reg_num}")
	if timetable:
		timetable_data = [entry.json for entry in timetable]
		return jsonify({'timetable': timetable_data})
	else:
		print(f"No timetable found for personnel_reg_num: {personnel_reg_num}")
		return jsonify({'error': 'Timetable not found'}), 404
	
# Delete a specific hour from the timetable
@employee_bp.route('/delete-timetable/delete-hour/<personnel_reg_num>', methods=['POST'])
def delete_hour():
	# This function should fetch the timetable for the employee and find the day the hour is in
	# then it should loop through the entries (intervals) for that day and look for the interval that contains the hour:
	# - If the interval is the same as the hour, remove it from the timetable
	# - If the interval contains the hour, split it into two intervals and remove the original interval
	# Keep in mind the edge cases where the interval starts or ends at the same time as the hour (e.g. hour = 08:00 - 09:00, interval = 08:00 - 12:00)
	pass

# Delete a specific day from the timetable
@employee_bp.route('/delete-timetable/delete-day/<personnel_reg_num>', methods=['POST'])
def delete_day():
	# This function should fetch the timetable for the employee and delete the entire day
	pass



####### EVENTS ROUTES #######
events_bp = Blueprint('events', __name__)

# Création du dossier QR codes si nécessaire
qr_codes_dir = os.path.join('static', 'qr_codes')
if not os.path.exists(qr_codes_dir):
	os.makedirs(qr_codes_dir)

@events_bp.route('/events', methods=['POST', 'GET'])
def events():
	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	hours = [f'{hour:02}:00 - ' for hour in range(23)] + ['23:00 - 00:00']
	employees = Personnel.query.filter_by(deleted=False).all()
	
	if request.method == 'POST':
		try:
			day = request.form.get('day')
			start_hour = request.form.get('start_hour')
			end_hour = request.form.get('end_hour')
			event = request.form.get('event')
			event_type = request.form.get('event_type')

			if not all([day, start_hour, end_hour, event, event_type]):
				return jsonify({'success': False, 'message': 'Missing data'}), 400

			event_obj = Event(day=day, start_hour=start_hour, end_hour=end_hour, event=event, event_type=event_type)
			db.session.add(event_obj)
			db.session.commit()

			qr_code_data = f'Event: {event}, Type: {event_type}, Day: {day}, Start: {start_hour}, End: {end_hour}'
			qr_code = qrcode.make(qr_code_data)
			qr_code_path = os.path.join(qr_codes_dir, f'event_{event_obj.id}.png')
			qr_code.save(qr_code_path)

			event_obj.qr_code_path = qr_code_path
			db.session.commit()

			# Option 1: Redirection après succès
			#return redirect(url_for('events.events'))
			return jsonify({'success': True, 'message': 'Event created successfully'}), 200

			# Option 2: Message de succès
			# return render_template('template.html', success_message='Event created successfully!')

		except Exception as e:
			db.session.rollback()
			return jsonify({'success': False, 'message': str(e)}), 500

	events = Event.query.all()
	schedule = {day: {hour: [] for hour in hours} for day in days}
	for event in events:
		start_index = hours.index(event.start_hour)
		end_index = hours.index(event.end_hour)
		if start_index <= end_index:
			for hour in hours[start_index:end_index + 1]:
				if (event.event, event.event_type) not in schedule[event.day][hour]:
					schedule[event.day][hour].append((event.event, event.event_type))
		else:
			for hour in hours[start_index:]:
				if (event.event, event.event_type) not in schedule[event.day][hour]:
					schedule[event.day][hour].append((event.event, event.event_type))
			next_day = days[(days.index(event.day) + 1) % 7]
			for hour in hours[:end_index + 1]:
				if (event.event, event.event_type) not in schedule[next_day][hour]:
					schedule[next_day][hour].append((event.event, event.event_type))
	
	return render_template('events.html', days=days, hours=hours, schedule=schedule, page='events', employees=employees)


@employee_bp.route('/camera')
def camera():
	return render_template('cameras.html',  cloudinary_url=cloudinary_url, page='cameras')