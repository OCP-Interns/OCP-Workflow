from flask import Flask, Blueprint, request
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import face_recognition

cam_bp = Blueprint('frame', __name__)

@cam_bp.route('/frame', methods=['POST'])
def proc_frame():
    image_data = request.form['image']

    header, encoded = image_data.split(",", 1)
    decoded = base64.b64decode(encoded)
    image = Image.open(BytesIO(decoded)).convert('RGB')

    frame = np.array(image)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    faces = face_recognition.face_locations(frame)
    if not faces:
        return 'mablanech'

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return 'blan'
