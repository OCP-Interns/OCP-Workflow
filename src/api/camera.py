from flask import Blueprint, Response, render_template
import cv2
import face_recognition

cam_bp = Blueprint('camera', __name__)

def generate_frames():
  pass