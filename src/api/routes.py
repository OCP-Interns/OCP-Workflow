from flask import Blueprint, request, render_template
from db import Personnel

dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

manage_bp = Blueprint('manage_employees', __name__)
@manage_bp.route('/manage-employees')
def manage_employees():
	employees = Personnel.query.filter_by(deleted=False).all()
	return render_template('manage.html', employees=employees)

add_bp = Blueprint('add_employee', __name__)
@add_bp.route('/add-employee', methods=['POST', 'GET'])
def add_employee():
	if request.method == 'POST':
		print('POST')
		#return render_template('add.html')
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
		return render_template('edit.html', employee=employee)
	else:
		print('GET')
		print(f'Showing employee with CIN: {cin}')
		return render_template('edit.html', employee=employee)

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