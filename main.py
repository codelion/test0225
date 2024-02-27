from flask import Flask, request, render_template_string, escape
import os

app = Flask(__name__)

@app.route('/view-file')
def view_file():
    file_name = request.args.get('file')  # User-supplied input without proper sanitization
    if file_name:
        # Ensure that the file_name does not contain path traversal characters
        file_name = os.path.basename(file_name)
    try:
        # Use a safe path to open the file
        safe_path = os.path.join('safe_directory', file_name)
        with open(safe_path, 'r') as file:
            content = file.read()
            # Escape the content to prevent XSS
            content = escape(content)
            return render_template_string('<h1>File Content</h1><pre>{{ content }}</pre>', content=content)
    except Exception as e:
        return render_template_string('<h1>Error</h1><p>Could not read file.</p>')

@app.route('/search')
def search():
    query = request.args.get('query')  # User-supplied input without proper escaping
    # Escape the query to prevent XSS
    query = escape(query)
    return render_template_string('<h1>Search Results</h1><p>No results found for: {{ query }}</p>', query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Properly escape the username to prevent XSS
        username = escape(username)
        
        # This is a mock SQL query to demonstrate vulnerability. In a real scenario, this would be executed against a database.
        # Use parameterized queries to prevent SQL injection
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        
        # Vulnerable SQL query execution (hypothetical)
        # For demonstration only. Do not execute SQL queries this way.
        print("Executing query: " + query)
        
        return render_template_string('<h1>Login Successful</h1><p>Welcome back, {{ username }}</p>', username=username)
    else:
        return '''
            <h1>Login</h1>
            <form method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
            '''

if __name__ == '__main__':
    app.run(debug=False)
