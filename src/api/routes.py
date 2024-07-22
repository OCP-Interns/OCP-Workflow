from flask import Blueprint, request, render_template, jsonify
from db import Personnel, TimeTable, db
from cloudinary.utils import cloudinary_url
import json

ping_bp = Blueprint('ping', __name__)
@ping_bp.route('/ping')
def ping():
	print('\033[92m + Pong\033[0m')
	return 'Pong', 200

dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

manage_bp = Blueprint('manage_employees', __name__)
@manage_bp.route('/manage-employees')
def manage_employees():
	employees = Personnel.query.filter_by(deleted=False).all()
	return render_template('manage.html', employees=employees, cloudinary_url=cloudinary_url)

add_bp = Blueprint('add_employee', __name__)
@add_bp.route('/add-employee', methods=['POST', 'GET'])
def add_employee():
	if request.method == 'POST':
		print('POST')
		return {'success': True, 'message': 'Employee added successfully'}, 200
	else:
		print('GET')
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

AddTableTime_bp = Blueprint('AddTableTime', __name__)
@AddTableTime_bp.route('/AddTableTime/<personnel_reg_num>', methods=['GET', 'POST'])
def AddTableTime(personnel_reg_num):
    if request.method == 'POST':
        timetable_json = request.form.get('timetable_json')
        if timetable_json:
            timetable_data = json.loads(timetable_json)
            new_entry = TimeTable(personnel_reg_num=personnel_reg_num, json=timetable_data)
            db.session.add(new_entry)
            db.session.commit()
            print('reg_num : ', personnel_reg_num, ' added by post method')
        return render_template('edit.html', employee=GetEMPBy_reg_num(personnel_reg_num), cloudinary_url=cloudinary_url)
    else:
        print('reg_num : ', personnel_reg_num, ' accessed by get method')
        return render_template('edit.html', employee=GetEMPBy_reg_num(personnel_reg_num), cloudinary_url=cloudinary_url)

def GetEMPBy_reg_num(reg_num):
    return Personnel.query.filter_by(reg_num=reg_num).first()

time_view_bp = Blueprint('timetable', __name__)
@time_view_bp.route('/timetable/<personnel_reg_num>', methods=['GET'])
def TimeView(personnel_reg_num):
    timetable = TimeTable.query.filter_by(personnel_reg_num=personnel_reg_num).all()
    print(f"Requested timetable for personnel_reg_num: {personnel_reg_num}")
    if timetable:
        timetable_data = [entry.json for entry in timetable]
        return jsonify({'timetable': timetable_data})
    else:
        print(f"No timetable found for personnel_reg_num: {personnel_reg_num}")
        return jsonify({'error': 'Timetable not found'}), 404
	
delete_tableTime = Blueprint('deleteTableTime', __name__)
@delete_tableTime.route('/deleteTableTime/<personnel_reg_num>', methods=['GET'])
	
def deleteTableTime():
	pass



