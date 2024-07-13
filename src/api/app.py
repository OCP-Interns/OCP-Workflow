from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import numpy as np
from addTimeLine import BpAdd

app = Flask(__name__)
app.register_blueprint(BpAdd)
CORS(app)

known_face_encodings = []
known_face_names = ["Mark Iplier"]
known_person_face_encoding = []


image_of_known_person = face_recognition.load_image_file("../../assets/mrf.jpg")
face_encodings = face_recognition.face_encodings(image_of_known_person)

if face_encodings:
	known_person_face_encoding = face_encodings[0]
else:
	print("ERROR: No faces were found in the image.")

known_face_encodings.append(known_person_face_encoding)

@app.route('/face-recognition', methods=['POST'])
def face_recognition_api():
	if 'file' not in request.files:
		return jsonify({'error': 'No file part'})
	
	file = request.files['file']

	if file.filename == '':
		return jsonify({'error': 'No selected file'})
	
	if file:
		image = face_recognition.load_image_file(file)
		face_locations = face_recognition.face_locations(image)
		face_encodings = face_recognition.face_encodings(image, face_locations)

		face_names = []
		for face_encoding in face_encodings:
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			name = "Unknown Person"

			face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = known_face_names[best_match_index]

			face_names.append(name)

		print('Found:', face_names)

		return jsonify({'face_names': face_names})

if __name__ == '__main__':
	app.run(debug=True)