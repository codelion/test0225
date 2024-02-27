from flask import Flask, request, render_template_string, escape

app = Flask(__name__)

@app.route('/view-file')
def view_file():
    file_name = request.args.get('file')  # User-supplied input without proper sanitization
    try:
        # Ensure that the file path is safe to open
        if '..' in file_name or file_name.startswith('/'):
            raise ValueError("Invalid file path")
        with open(file_name, 'r') as file:
            content = file.read()
            # Escape any user-provided content before rendering
            return render_template_string('<h1>File Content</h1><pre>' + escape(content) + '</pre>')
    except Exception as e:
        return render_template_string('<h1>Error</h1><p>Could not read file.</p>')

@app.route('/search')
def search():
    query = request.args.get('query')  # User-supplied input without proper escaping
    # Escape any user-provided content before rendering
    return render_template_string('<h1>Search Results</h1><p>No results found for: ' + escape(query) + '</p>')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # This is a mock SQL query to demonstrate vulnerability. In a real scenario, this would be executed against a database.
        # Ensure that the dynamic object attribute is properly controlled
        query = escape("SELECT * FROM users WHERE username = '") + escape(username) + escape("' AND password = '") + escape(password) + escape("'")
        
        # Vulnerable SQL query execution (hypothetical)
        # Remove active debug code
        # print("_Constant_16_" + _Name_4_)
        
        # Escape any user-provided content before rendering
        return render_template_string('<h1>Login Successful</h1><p>Welcome back, ' + escape(username) + '!</p>')
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
    app.run(debug=False)  # Disable debug mode
