from flask import Flask, Blueprint, request
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import face_recognition
import os
import glob
from datetime import datetime

known_faces = []
known_names = []
face_detected_time = None
face_detected_timeLeaving = None
arrive = []
depart = []
duration_list = []
day = None
faces_folder = 'C:/Users/marou/OneDrive/Desktop/OCP-Workflow-mrf/faces/'



def get_encoding(img):
    image = face_recognition.load_image_file(img)
    face_encoding = face_recognition.face_encodings(image)
    if len(face_encoding) > 0:
        return face_encoding[0]
    return "no fuond on the folder"

def filtering_img(faces_folder):
    if os.path.exists(faces_folder):
        for name in os.listdir(faces_folder):
            images = os.path.join(faces_folder, name, '*.jpg')
            images_path = glob.glob(images)
            for image in images_path:
                encoding = get_encoding(image)
                if encoding is not None:
                    known_faces.append(encoding)
                    known_names.append(name)
                else:
                    return 'no data found'
    else:
        return 'path not fuond'

filtering_img(faces_folder)

cam_bp = Blueprint('frame', __name__)

@cam_bp.route('/frame', methods=['POST'])
def proc_frame():
    global face_detected_time, face_detected_timeLeaving, day
    
    try:
        image_data = request.form['image']
        header, encoded = image_data.split(",", 1)
        decoded = base64.b64decode(encoded)
        image = Image.open(BytesIO(decoded)).convert('RGB')

        frame = np.array(image)
        faces = face_recognition.face_locations(frame)
    
        if not faces:
            return 'No faces detected'

        names = []
        
        for face in faces:
            encoding = face_recognition.face_encodings(frame, [face])[0]
            matches = face_recognition.compare_faces(known_faces, encoding)
            
            if True in matches:
                first_match = matches.index(True)
                name = known_names[first_match]
                names.append(name)
        
        time_message = update_time(len(faces) > 0)
        
        return f'Face recognized: {names} matches found //// timing : {time_message}'

    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500

def update_time(face):
    global face_detected_time, face_detected_timeLeaving, day
    
    if face:
        if face_detected_time is None:
            face_detected_time = datetime.now()
            day = face_detected_time.date()
            arrive.append(face_detected_time)
             
        else:
            face_detected_timeLeaving = datetime.now()
            day = face_detected_timeLeaving.date()
            depart.append(face_detected_timeLeaving)
        
        duratin_message = calculate_duration(arrive, depart)
        return f"Face detected at: {min(arrive)} on {day} and face leving at: {max(depart)} on {day}, duration: {duratin_message}"

    return "no face detected"
            
def calculate_duration(arrive, depart):
    if arrive and depart:
        min_arriv = min(arrive)
        max_dep = max(depart)
        
        duree = max_dep - min_arriv
        
        duration_list.append(duree)
        
        return f"duration detecting face: {max(duration_list)}"
    
    return '_'