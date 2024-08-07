from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def init_db(app):
	load_dotenv()

	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI').replace('mysql://', 'mysql+pymysql://')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
	
	db.init_app(app)

	with app.app_context():
		db.create_all()
		print('\033[92m + Database initialized successfully\033[0m')

	return db

class Personnel(db.Model):
	__tablename__ = 'personnel'
	reg_num = db.Column(db.String(255), primary_key=True)
	photo = db.Column(db.String(255), nullable=False)
	cin = db.Column(db.String(255), unique=True)

	first_name = db.Column(db.String(255), nullable=False)
	last_name = db.Column(db.String(255), nullable=False)
	phone = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)
	shift = db.Column(db.String(255), nullable=False) # Values: 'normal', 'split', 'rotating'

	deleted = db.Column(db.Boolean, nullable=False, default=False)
	is_admin = db.Column(db.Boolean, nullable=False, default=False)

class TimeTable(db.Model):
	__tablename__ = 'timetable'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	personnel_reg_num = db.Column(db.String(255), db.ForeignKey('personnel.reg_num'), nullable=False)
	json = db.Column(db.JSON, nullable=False)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(255), nullable=False)
    start_hour = db.Column(db.String(255), nullable=False)
    end_hour = db.Column(db.String(255), nullable=False)
    event = db.Column(db.String(255), nullable=False)
    event_type = db.Column(db.String(255), nullable=False)
    qr_code_path = db.Column(db.String(255), nullable=True)
        
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def init_db(app):
	load_dotenv()

	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI').replace('mysql://', 'mysql+pymysql://')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
	
	db.init_app(app)

	with app.app_context():
		db.create_all()
		print('\033[92m + Database initialized successfully\033[0m')

	return db

class Personnel(db.Model):
	__tablename__ = 'personnel'
	reg_num = db.Column(db.String(255), primary_key=True)
	photo = db.Column(db.String(255), nullable=False)
	cin = db.Column(db.String(255), unique=True)

	first_name = db.Column(db.String(255), nullable=False)
	last_name = db.Column(db.String(255), nullable=False)
	phone = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)
	shift = db.Column(db.String(255), nullable=False) # Values: 'normal', 'split', 'rotating'

	deleted = db.Column(db.Boolean, nullable=False, default=False)
	is_admin = db.Column(db.Boolean, nullable=False, default=False)

class TimeTable(db.Model):
	__tablename__ = 'timetable'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	personnel_reg_num = db.Column(db.String(255), db.ForeignKey('personnel.reg_num'), nullable=False)
	json = db.Column(db.JSON, nullable=False)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(255), nullable=False)
    start_hour = db.Column(db.String(255), nullable=False)
    end_hour = db.Column(db.String(255), nullable=False)
    event = db.Column(db.String(255), nullable=False)
    event_type = db.Column(db.String(255), nullable=False)
    qr_code_path = db.Column(db.String(255), nullable=True)
        
class DurationWorked(db.Model):  
    __tablename__ = 'duration_worked'  
    id = db.Column(db.Integer, primary_key=True)
    personnel_reg_num = db.Column(db.String(255), db.ForeignKey('personnel.reg_num'), nullable=False)
    day_in = db.Column(db.String(255), nullable=False)
    day_off = db.Column(db.String(255), nullable=False)
    time_in = db.Column(db.String(255), nullable=False)
    time_off = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)