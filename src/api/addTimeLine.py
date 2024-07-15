from flask import Flask, request, jsonify, Blueprint
from connection import connection

app = Flask(__name__)


BpAdd = Blueprint('add', __name__)

@BpAdd.route('/addTime', methods=['POST'])

def add_time_work():

    data = request.form
    day = data.get('day')
    from_time = data.get('from')
    to_time = data.get('to')

    query = "INSERT INTO TableTimeEmp (day, From_h, To_h) VALUES (%s, %s, %s)"
    cursor = connection.cursor()

    try:
        cursor.execute(query, (day, from_time, to_time))
        connection.commit()
        return jsonify({"message": "Time added successfully"}), 200
    
    except Exception as e:

        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:

        cursor.close()


BpSelect = Blueprint('selectTable', __name__)

@BpSelect.route('/SelectTable', methods=['GET'])

def selectTable():
    query = "SELECT day, From_h, To_h FROM TableTimeEmp"
    cursor = connection.cursor()  
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        timetable = []
        for row in results:
            timetable.append({
                "day": row[0],
                "from": row[1],
                "to": row[2]
            })
        return jsonify({"timetable": timetable}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()



