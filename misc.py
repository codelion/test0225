from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Insecure SQL query construction
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    connection