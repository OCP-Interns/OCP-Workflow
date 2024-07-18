from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import numpy as np
from addTimeLine import BpAdd, BpSelect, BpDelete

app = Flask(__name__)
app.register_blueprint(BpAdd)
app.register_blueprint(BpSelect)
app.register_blueprint(BpDelete)
CORS(app)

if __name__ == '__main__':
	app.run(debug=True)