from flask import Flask, request, jsonify, Blueprint
from connection import connection 
from datetime import datetime, timedelta

app = Flask(__name__)

BpAdd = Blueprint('add', __name__)
BpSelect = Blueprint('selectTable', __name__)
BpDelete = Blueprint('delete', __name__)

@BpAdd.route('/addTime', methods=['POST'])
def add_time_work():
    data = request.json
    day = data.get('day')
    from_time = data.get('from')
    to_time = data.get('to')
    print('day: ', day)
    print('from: ', from_time)
    print('to: ', to_time)

    from_time_dt = datetime.strptime(from_time, '%H:%M')
    to_time_st = datetime.strptime(to_time, '%H:%M')

    time_slots = []
    while from_time_dt < to_time_st:
        next_hour = from_time_dt + timedelta(hours=1, minutes=1)
        next_hour_str = next_hour.strftime('%H:%M')
        time_slots.append((day, from_time_dt.strftime('%H:%M'), next_hour_str))
        from_time_dt = next_hour

    query = "INSERT INTO TableTimeEmp (day, From_h, To_h) VALUES (%s, %s, %s)"
    cursor = connection.cursor()

    try:  
        for slot in time_slots:
            cursor.execute(query, slot)
            connection.commit()
        return jsonify({"message": 'blan'}), 200
    
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()

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

@BpDelete.route('/DeleteWork', methods=['POST'])  
def deletWork():
    data = request.form
    day = data.get('day')
    from_ = data.get('from')

    query = "DELETE FROM TableTimeEmp WHERE day=%s AND From_h=%s"
    cursor = connection.cursor()

    try:
        cursor.execute(query, (day, from_))
        connection.commit()
        return jsonify({'message' :'Deleted successfully'}), 200
    
    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()