from flask import Flask, Blueprint, request, jsonify
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import face_recognition
import os
import glob
from datetime import datetime
from db import DurationWorked, db, Personnel
import pandas as pd

# Global variables for face recognition and time tracking
known_faces = []
known_names = []
face_detected_time = None
face_detected_timeLeaving = None
arrive = []
depart = []
duration_list = []
day_in = None
day_off = None
faces_folder = 'C:/Users/marou/OneDrive/Desktop/OCP-Workflow-mrf/faces/'

# Function to get face encoding from an image file
def get_encoding(img):
    image = face_recognition.load_image_file(img)
    face_encoding = face_recognition.face_encodings(image)
    if len(face_encoding) > 0:
        return face_encoding[0]
    return None

# Function to filter and load face encodings from a folder
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
                    print(f"No data found for image: {image}")
    else:
        print(f"Path not found: {faces_folder}")

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
            return jsonify({"msg": 'No faces detected'})

        names = []
        
        for face in faces:
            encoding = face_recognition.face_encodings(frame, [face])[0]
            matches = face_recognition.compare_faces(known_faces, encoding)
            
            if True in matches:
                first_match = matches.index(True)
                name = known_names[first_match]
                names.append(name)
        
        time_message = update_time(len(names) > 0)  # Corrected to len(names)
        
        return jsonify({'message': f'Face recognized: {names} matches found', 'timing': time_message})

    except Exception as e:
        return jsonify({'error': f"Internal Server Error: {str(e)}"}), 500

def update_time(face):
    global face_detected_time, face_detected_timeLeaving, day_in, day_off
    
    if face:
        if face_detected_time is None:
            face_detected_time = datetime.now()
            day_in = face_detected_time.date()
            arrive.append(face_detected_time)
             
        else:
            face_detected_timeLeaving = datetime.now()
            day_off = face_detected_timeLeaving.date()
            depart.append(face_detected_timeLeaving)
        
        duration_message = calculate_duration(min(arrive), max(depart), face, day_in, day_off)  # Fixed typo
        return f"Face detected at: {min(arrive)} on {day_in} and face leaving at: {max(depart)} on {day_off}, duration: {duration_message}"

    return "No face detected"
            
def calculate_duration(arrive, depart, name, day_in, day_off):
    if arrive and depart:
        duration = depart - arrive  # Corrected variable name
        duration_list.append(duration)
        save_to_DB(arrive, depart, max(duration_list), name, day_in, day_off)
        save_to_excel(arrive, depart, max(duration_list), name, day_in, day_off)
        
        return f"Duration detecting face: {max(duration_list)}"
    
    return '_'

def save_to_DB(arrive, depart, duration_list, name, day_in, day_off):
    day_in_str = day_in.strftime('%Y-%m-%d')
    day_off_str = day_off.strftime('%Y-%m-%d') if day_off else None
    arrive_str = arrive.strftime('%H:%M:%S') 
    depart_str = depart.strftime('%H:%M:%S') if depart else None
    
    if not personnel_exist(name):
        return f"reg_name {name} is not in"

    record = DurationWorked(
        personnel_reg_num=name,
        day_in=day_in_str,
        day_off=day_off_str,
        time_in=arrive_str,
        time_off=depart_str,
        duration=str(duration_list)
    )
    
    try:
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Failed to save to DB: {e}")
        return str(e)
    
def personnel_exist(name):
    return db.session.query(Personnel).filter_by(reg_num=name).first() is not None

def save_to_excel(arrive, depart, duration_list, name, day_in, day_off):
    try:
        duration_str = [str(d) for d in duration_list] if duration_list else 'N/A'
        table = {
            'reg_num': [name],
            'arrival time': [arrive],
            'depart': [depart],
            'dayIn': [day_in],
            'dayOff': [day_off],
            'duration': [', '.join(duration_str)]
        }
        
        df = pd.DataFrame(table)
        filename = 'attendance_data.xlsx'
        
        df.to_excel(filename, index=False, engine='openpyxl')
        
        print(f"Data successfully written to {filename}")

    except Exception as e:
        print(f"Failed to save to Excel: {e}")
        raise
