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
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute(query)  # Execution of unsanitized input
    result = cursor.fetchone()
    if result:
        return 'Login Successful!'
    else:
        return 'Login Failed!'

@app.route('/comment', methods=['GET'])
def comment():
    user_input = request.args.get('text')
    return render_template_string(f'User comment: {user_input}')  # Directly rendering user input without sanitization

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    command = f"ping -c 1 {host}"  # Taking a host parameter directly from user input
    result = os.popen(command).read()  # Executing the command without validation or sanitization
    return f'<pre>{result}</pre>'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join('uploads', filename)
    file.save(file_path)  # Saving the file without checking its content, leading to potential arbitrary file upload
    return f'File uploaded successfully to {file_path}.'

if __name__ == '__main__':
    app.run(debug=True)
