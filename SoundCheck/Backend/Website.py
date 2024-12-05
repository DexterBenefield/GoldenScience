from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from UserProfile import Base, UserProfile  # Import your SQLAlchemy models
from ConcertFinder import compileConcerts
from RatingDatabase import Rating, Base
from spotipy import create_spotify_instance, get_user_top_items
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

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
        return redirect(url_for('spotify_login'))  # Redirect to homepage after saving profile
    else:
        flash("User not found.")
        return redirect(url_for('create_profile_page'))

@app.route('/spotify/login')
def spotify_login():
    sp_oauth = SpotifyOAuth(
        client_id='cc68db0bcbf14ddcbc5f1a742c3ea215',
        client_secret='b37f65f0812e45a398bde333da674671',
        redirect_uri='http://127.0.0.1:5000/spotify/callback',
        scope='user-top-read',
        cache_handler=FlaskSessionCacheHandler(session)
    )
    if not sp_oauth.get_cached_token():
        return redirect(sp_oauth.get_authorize_url())
    return redirect(url_for('homepage'))

@app.route('/spotify/callback')
def spotify_callback():
    sp_oauth = SpotifyOAuth(
        client_id='cc68db0bcbf14ddcbc5f1a742c3ea215',
        client_secret='b37f65f0812e45a398bde333da674671',
        redirect_uri='http://127.0.0.1:5000/spotify/callback',
        scope='user-top-read',
        cache_handler=FlaskSessionCacheHandler(session)
    )
    code = request.args.get('code')
    if code:
        sp_oauth.get_access_token(code)
        flash("Spotify login successful!")
        return redirect(url_for('homepage'))  # Redirect to the homepage after successful authorization
    flash("Spotify login failed.")
    return redirect(url_for('homepage'))
    
@app.route('/homepage', methods = ['GET'])
def homepage():
    return render_template('homepage.html')

#@app.route('/reviews', methods = ['GET'])
#def reviews():
#    return render_template('reviews.html')

@app.route('/concerts' , methods=['GET', 'POST'])
def Concerts():
    concerts = compileConcerts()
    return render_template('concertFinder.html', concerts = concerts)
@app.route('/account' , methods = ['GET','POST'])
def account():
    username = session.get('username')  
    if username:
        user = db_session.query(UserProfile).filter_by(username=username).first()
        if user:
            user_data = user.display_profile() 
            return render_template('profilePage.html', user=user_data)
        else:
            flash("User not found.")
    else:
        flash("You must log in to access this page.")
        return redirect(url_for('login_page'))

    return render_template('profilePage.html', user=None)
@app.route('/userposts', methods = ['GET','POST'])
def individualposts():
    username = session.get('username')  
    if username:
        user = db_session.query(UserProfile).filter_by(username=username).first()
        if user:
            user_data = user.display_profile() 
            user_reviews = user.reviews
            return render_template('individualPosts.html', user=user_data)
        else:
            flash("User not found.")
    else:
        flash("You must log in to access this page.")
        return redirect(url_for('login_page'))
@app.route('/leave-a-rating', methods=['GET'])
def giveRating():
    return render_template('ReviewPage.html')
@app.route('/leave-a-rating', methods=['POST'])
def submitReview():
    
        user_id = session.get('username')  # Ensure user_id or username is stored in the session
        if not user_id:
            flash("You must be logged in to leave a review.")
            return redirect(url_for('login_page'))

        review_text = request.form.get('review')
        location = int(request.form.get('location'))  # This matches the `name="location"` in the HTML
        parking = int(request.form.get('parking'))
        merch = int(request.form.get('merch'))
        sound_quality = int(request.form.get('sound_quality'))
        set_list = int(request.form.get('set_list'))
        ticket_price = int(request.form.get('ticket_price'))
        facilities = int(request.form.get('facilities'))
        security = int(request.form.get('security'))
        average_rating = float(request.form.get('average'))

        # Create a new Rating instance
        new_review = Rating(
            user_id=user_id,
            review_text=review_text,
            location_rating=location,
            parking_rating=parking,
            merch_rating=merch,
            sound_quality_rating=sound_quality,
            set_list_rating=set_list,
            ticket_price_rating=ticket_price,
            facilities_rating=facilities,
            security_rating=security,
            average_rating= average_rating
        )

        # Add to the database
        db_session.add(new_review)
        db_session.commit()
        return redirect(url_for('homepage'))
    
if __name__ == '__main__':
    app.run(debug=True)
