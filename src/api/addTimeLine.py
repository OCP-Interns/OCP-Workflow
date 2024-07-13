from flask import Flask, request, jsonify, Blueprint

BpAdd = Blueprint('add', __name__)

@BpAdd.route('/addTime', methods=['Post'])

def add_time_work():
    data = request.form
    day = data.get('day') 
    from_time = data.get('from') 
    to_time = data.get('to')  
    
   
