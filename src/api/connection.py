import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='bcqkw1nmvy6embwex6i5-mysql.services.clever-cloud.com',
        database='bcqkw1nmvy6embwex6i5',
        user='uuamb2qozqulxtk5',
        password='zdaQnAxlHkA4S0PNqOqv'
    )
    print('blan')
except Error as error:
    print('Error connection: ', error)
