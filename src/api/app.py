import face_recognition

from db import init_db
from sign_in import sign_in_bp
from routes import general_bp, employee_bp
from init import *

def create_app():	
	cors.init_app(app)
	bcrypt.init_app(app)
	db = init_db(app)

	app.register_blueprint(sign_in_bp)
	app.register_blueprint(general_bp)
	app.register_blueprint(employee_bp)
	
	return app, db

app, db = create_app()

from db import Personnel
from cloudinary.utils import cloudinary_url
from urllib.request import urlopen

# Insert the default personnel data
with app.app_context():
	if not Personnel.query.first():
		db.session.add(Personnel(
			photo='TT123456',
			cin='HH123456',

			first_name='Someone',
			last_name='Guy',
			reg_num='IT123456',
			phone='123456',
			email='someguy@gmail.com',
			password=bcrypt.generate_password_hash('123456').decode('utf-8'),
			shift='normal',

			deleted=False,
			is_admin=True
		))
		db.session.commit()
		print('\033[92m + Default user inserted successfully\033[0m')
	else:
		print('\033[94m - Default user already exists\033[0m')

if __name__ == '__main__':
	app.run(debug=True)