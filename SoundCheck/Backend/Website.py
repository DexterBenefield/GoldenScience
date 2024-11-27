from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from UserProfile import Base, UserProfile  # Import your SQLAlchemy models
import Concert
from ConcertFinder import compileConcerts
app = Flask(__name__,template_folder='Webpages')

app.secret_key = 'your_unique_secret_key'

# Database setup
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()



# Route to serve the registration page
@app.route('/', methods=['GET' , 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        # Fetch the user from the database
        user = db_session.query(UserProfile).filter_by(username=username).first()
        
        if user and user.password == password:  # Validate password
            session['username'] = user.username  # Set username in session
            flash("Success! Login complete.")
            return redirect(url_for('homepage'))  # Redirect to the homepage
        else:
            # Incorrect username or password
            flash("Incorrect username or password.")
    
    # Render login page for GET requests or after a failed login
    return render_template('index.html')
    
@app.route('/logout', methods = [ 'GET'])
def logout():
    session.clear()
    flash("Logged Out Succesfull!")
    return redirect(url_for('login_page'))



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
        return redirect(url_for('create_profile_page'))  # Redirect to create profile
    except IntegrityError:
        db_session.rollback()
        return jsonify({"success": False, "message": "Username or email already exists."})

    
@app.route('/create-profile', methods = ['GET'])
def create_profile_page():
    return render_template('create_profile.html')

@app.route('/save-profile', methods=['POST'])
def save_profile():
    if 'username' not in session:
        return redirect(url_for('login_page'))  # Redirect to the login page if not logged in

    data = request.form
    username = session['username']  # Get the logged-in username

    user = db_session.query(UserProfile).filter_by(username=username).first()

    if user:
        # Update user profile
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.bio = data.get('bio')
        user.location = data.get('location')
        user.favorite_artists = data.get('favorite_artists', '')
        user.favorite_genres = data.get('favorite_genres', '')

        # Handle profile picture upload
        profile_pic = request.files.get('profile_pic')
        if profile_pic:
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            profile_pic_path = os.path.join(upload_folder, profile_pic.filename)
            profile_pic.save(profile_pic_path)
            user.profile_pic = profile_pic_path

        db_session.commit()
        return redirect(url_for('homepage'))  # Redirect to homepage after saving profile
    else:
        flash("User not found.")
        return redirect(url_for('create_profile_page'))
    
@app.route('/homepage', methods = ['GET'])
def homepage():
    return render_template('homepage.html')

@app.route('/concerts' , methods=['GET', 'POST'])
def Concerts():
    concerts = compileConcerts()
    return render_template('concertFinder.html', concerts = concerts)


if __name__ == '__main__':
    app.run(debug=True)
