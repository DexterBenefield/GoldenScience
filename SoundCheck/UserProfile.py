from sqlalchemy import create_engine, Column, Integer, String, JSON, PickleType, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Database engine and base class
engine = create_engine('sqlite:///app.db')
Base = declarative_base()

# UserProfile class definition
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    location = Column(String)
    bio = Column(String)
    visibility = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    profile_pic = Column(String)
    social_links = Column(JSON)
    favorite_genres = Column(PickleType)
    favorite_artists = Column(PickleType)
    upcoming_concerts = Column(PickleType)
    attended_concerts = Column(PickleType)
    reviews = Column(PickleType)

    def __init__(self, username, email, location, first_name=None, last_name=None, 
                 profile_pic=None, bio=None, social_links=None, 
                 favorite_genres=None, favorite_artists=None, 
                 upcoming_concerts=None, attended_concerts=None, 
                 reviews=None, visibility="public"):
        self.username = username
        self.email = email
        self.location = location
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic
        self.bio = bio
        self.social_links = social_links if social_links else {}
        self.favorite_genres = favorite_genres if favorite_genres else []
        self.favorite_artists = favorite_artists if favorite_artists else []
        self.upcoming_concerts = upcoming_concerts if upcoming_concerts else []
        self.attended_concerts = attended_concerts if attended_concerts else []
        self.reviews = reviews if reviews else []
        self.visibility = visibility

    # Add user profile to the database
    def add_user_profile(self, session):
        try:
            session.add(self)
            session.commit()
        except IntegrityError:
            session.rollback() 
            print("User profile with this email already exists.")

    # Update profile information
    def update_profile(self, new_email=None, new_location=None, new_first_name=None, 
                       new_last_name=None, new_bio=None, new_visibility=None):
        if new_email:
            self.email = new_email
        if new_location:
            self.location = new_location
        if new_first_name:
            self.first_name = new_first_name
        if new_last_name:
            self.last_name = new_last_name
        if new_bio:
            self.bio = new_bio
        if new_visibility:
            self.visibility = new_visibility

    # Add a favorite artist
    def add_favorite_artist(self, artist_name):
        if artist_name not in self.favorite_artists:
            self.favorite_artists.append(artist_name)

    # Add a favorite genre
    def add_favorite_genre(self, genre):
        if genre not in self.favorite_genres:
            self.favorite_genres.append(genre)

    # Add an upcoming concert
    def add_upcoming_concert(self, concert):
        if concert not in self.upcoming_concerts:
            self.upcoming_concerts.append(concert)

    # Add a review
    def add_review(self, concert, review_text, rating):
        review = {
            "concert": concert,
            "review_text": review_text,
            "rating": rating
        }
        self.reviews.append(review)

    # Display profile information
    def display_profile(self):
        return {
            'Username': self.username,
            'First Name': self.first_name,
            'Last Name': self.last_name,
            'Email': self.email,
            'Location': self.location,
            'Bio': self.bio,
            'Favorite Artists': self.favorite_artists,
            'Favorite Genres': self.favorite_genres,
            'Upcoming Concerts': self.upcoming_concerts,
            'Attended Concerts': self.attended_concerts,
            'Reviews': self.reviews,
            'Visibility': self.visibility
        }