import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='bcqkw1nmvy6embwex6i5-mysql.services.clever-cloud.com',
        database='bcqkw1nmvy6embwex6i5',
        user='uuamb2qozqulxtk5',
        password='zdaQnAxlHkA4S0PNqOqv'
    )
    if connection.is_connected():
        print('Connected to MySQL database')
except Error as e:
    print(f"Error connecting to MySQL database: {e}")
