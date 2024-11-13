from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from UserProfile import Base, UserProfile  # Import your SQLAlchemy models

app = Flask(__name__,template_folder='AccountHandling')

# Database setup
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/")
def home():
    return render_template("index.html")

# Route to serve the registration page
@app.route('/login', methods=['POST'])
def login_page():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    user = session.query(UserProfile).filter_by(username=username).first()
    if user and user.password == password:  # Compare plain text passwords
        # Password matches
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        # Incorrect username or password
        return jsonify({"success": False, "message": "Invalid username or password."})


# Route to serve the registration page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')  # Make sure register.html is in the "templates" folder

# Route to handle form submissions
@app.route('/register', methods=['POST'])
def register_user():
    data = request.form  # Get form data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    location = data.get('location', '')  # Optional field

    # Create a new user profile
    new_user = UserProfile(
        username=username,
        email=email,
        location=location,
        password = password,
        first_name='',  # Set default values if needed
        last_name='',
        bio='',
        profile_pic=None,
        visibility="public"
    )

    # Add the user to the database
    try:
        new_user.add_user_profile(session)
        return jsonify({"success": True, "message": "Registration successful!"})
    except IntegrityError:
        return jsonify({"success": False, "message": "Username or email already exists."})

if __name__ == '__main__':
    app.run(debug=True)

