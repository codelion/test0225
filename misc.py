from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key'  # Set a secret key for CSRF protection

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Secure SQL query construction using parameterized queries
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute(query, (username, password))  # Execution of parameterized query
    result = cursor.fetchone()
    if result:
        return 'Login Successful!'
    else:
        return 'Login Failed!'

@app.route('/comment', methods=['GET'])
def comment():
    user_input = request.args.get('text')
    # Use the escape function to prevent XSS
    user_input_escaped = render_template_string('{{ user_input }}', user_input=user_input)
    return f'User comment: {user_input_escaped}'

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    # Validate or sanitize the host parameter to prevent command injection
    # For demonstration, we'll just allow localhost pings
    if host == 'localhost':
        command = f"ping -c 1 {host}"
        result = os.popen(command).read()
        return f'<pre>{result}</pre>'
    else:
        return 'Invalid host'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    # Ensure the filename is secure before saving it
    filename = secure_filename(filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    return f'File uploaded successfully to {file_path}.'

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode for production
