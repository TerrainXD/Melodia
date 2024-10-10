# backend/database.py
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="your_database_name"
)

if connection.is_connected():
    print("Connected to MySQL!")
