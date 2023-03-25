import mysql.connector

global cursor
global connection

connection = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="",
    database="notewave",
)

cursor = connection.cursor(dictionary=True)



        