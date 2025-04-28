from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for sessions

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Basic route
@app.route('/')
def home():
    return 'Hello, World!'

# Route with variable
@app.route('/user/<username>')
def show_user(username):
    return f'User: {username}'

# Multiple HTTP methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            session['user'] = username
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

# Protected route example
@app.route('/dashboard')
@login_required
def dashboard():
    return 'Welcome to dashboard'

# JSON response
@app.route('/api/data')
def get_data():
    data = {'name': 'John', 'age': 30}
    return jsonify(data)

# Query parameters
@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f'Search query: {query}'

# Form handling
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    return f'Submitted: {name}, {email}'

# File upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded'
    file = request.files['file']
    file.save('uploads/' + file.filename)
    return 'File uploaded successfully'

# Error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Before request
@app.before_request
def before_request():
    if 'counter' not in session:
        session['counter'] = 0
    session['counter'] += 1

# Template with context
@app.route('/template')
def template_example():
    return render_template('example.html', 
                         title='Flask Example',
                         items=['one', 'two', 'three'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)