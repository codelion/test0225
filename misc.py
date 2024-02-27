from flask import Flask, request, render_template_string, escape
import sqlite3
import os

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Insecure SQL query construction
    query = "?"
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute(query, (username, password))  # Execution of unsanitized input
    result = cursor.fetchone()
    if result:
        return 'Login Successful!'
    else:
        return 'Login Failed!'

@app.route('/comment', methods=['GET'])
def comment():
    user_input = request.args.get('text')
    user_input = escape(user_input)
    return render_template_string(f'User comment: {user_input}')  # Directly rendering user input without sanitization

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    host = escape(host)
    command = f"ping -c 1 {host}"  # Taking a host parameter directly from user input
    result = os.popen(command).read()  # Executing the command without validation or sanitization
    result = escape(result)
    return f'<pre>{result}</pre>'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = escape(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)  # Saving the file without checking its content, leading to potential arbitrary file upload
    file_path = escape(file_path)
    return f'File uploaded successfully to {file_path}.'

if __name__ == '__main__':
    app.run(debug=False)
