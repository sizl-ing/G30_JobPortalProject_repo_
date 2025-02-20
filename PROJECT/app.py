from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a real secret key in production
# Database configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Ensure this column exists

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password  # Set the password

    def save_hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    


# Create the database and tables

# Home page
@app.route('/')
def home():
    return render_template('index.html')  # Render index.html as the home page

# Find Jobs page
@app.route('/find_jobs')
def find_jobs():
    return render_template('jobs.html')

# Companies page
@app.route('/companies')
def companies():
    return render_template('Companies.html')

# Resources page
@app.route('/resources')
def resources():
    return render_template('resources.html')

# Post a Job page
@app.route('/post_job')
def post_job():
    return render_template('post-job.html')

# Login page
@app.route('/login')
def login_page():
    return render_template('login.html')  # Render login.html for the login page

# Login form submission
@app.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_email'] = user.email
        session['user_name'] = user.name
        flash('Login successful!', 'success')
        return redirect(url_for('home'))  # Redirect to home page after login
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('login_page'))  # Redirect back to the login page

# Index page (protected route)
@app.route('/index')
def index():
    if 'user_email' in session:
        return render_template('index.html', user_name=session['user_name'])
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login_page'))

# Logout
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_name', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(name,email,hashed_password)

        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login_page'))

    return render_template('signup.html')



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 