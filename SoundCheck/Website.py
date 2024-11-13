from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
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
db_session = Session()

@app.route("/")
def home():
    return render_template("index.html")

# Route to serve the registration page
@app.route('/', methods=['GET' , 'POST'])
def login_page():
    if request.method == ['POST']:
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = db_session.query(UserProfile).filter_by(username=username).first()
        if user and user.password == password:  # Compare plain text passwords
            session['username'] = user.username
            # Password matches
            return render_template('homepage.html')
        else:
            # Incorrect username or password
            return jsonify({"success": False, "message": "Invalid username or password."})
    return render_template('index.html')


# Route to serve the registration page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')  

# Route to handle form submissions
@app.route('/register', methods=['POST'])
def register_user():
    data = request.form  # Get form datas
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
        new_user.add_user_profile(db_session)
        return redirect(url_for('create_profile_page'))
    except IntegrityError:
        db_session.rollback()
        return jsonify({"success": False, "message": "Username or email already exists."})
    
@app.route('/create-profile', methods = ['GET'])
def create_profile_page():
    return render_template('create_profile.html')

@app.route('/save-profile', methods=['POST'])
def save_profile():
    if 'username' not in session:
        return jsonify({"success": False, "message": "User not logged in."})

    data = request.form
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    bio = data.get('bio')
    location = data.get('location')
    favorite_artists = data.get('favorite_artists')
    favorite_genres = data.get('favorite_genres')

    # Handle profile picture upload
    profile_pic = request.files.get('profile_pic')
    if profile_pic:
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        profile_pic_path = os.path.join(upload_folder, profile_pic.filename)
        profile_pic.save(profile_pic_path)
    else:
        profile_pic_path = None

    # Example: Retrieve the user from the database (replace 'example_user' with dynamic logic)
    user = db_session.query(UserProfile).filter_by(username='example_user').first()
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.bio = bio
        user.location = location
        user.profile_pic = profile_pic_path
        user.favorite_artists = favorite_artists.split(', ')
        user.favorite_genres = favorite_genres.split(', ')

        db_session.commit()
        return jsonify({"success": True, "message": "Profile created successfully!"})
    else:
        return jsonify({"success": False, "message": "User not found."})
@app.route('/homepage', methods = ['GET'])
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)
