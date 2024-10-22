from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Use the same engine and Base as UserProfile
engine = create_engine('sqlite:///app.db')
Base = declarative_base()

# Initialize concert details with artist name, venue, and date
class Concert(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String)
    venue = Column(String)
    date = Column(Date)
    overall_rating = Column(Float)

    def __init__(self, artist_name, venue, date):
        self.artist_name = artist_name
        self.venue = venue
        # Convert the date string to a datetime object
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.ratings = {
            'venue': None,
            'sound_quality': None,
            'seating': None,
            'merch': None,
            'parking': None,
            'food_and_drinks': None
        }
        self.review = None

    # Add this method to insert concert into the database
    def add_concert(self, session):
        session.add(self)
        session.commit()

    # Add a rating to a specific aspect of the concert
    def add_rating(self, category, rating):
        if category in self.ratings and 0 <= rating <= 5:
            self.ratings[category] = rating
            # Update overall_rating
            self.overall_rating = self.get_overall_rating()

    # Add a review for the concert
    def add_review(self, review):
        self.review = review

    # Calculate the average rating across all rated aspects
    def get_overall_rating(self):
        rated_items = [r for r in self.ratings.values() if r is not None]
        return sum(rated_items) / len(rated_items) if rated_items else None

    # Return the concert details and ratings as a dictionary
    def display_concert_details(self):
        return {
            'Artist': self.artist_name,
            'Venue': self.venue,
            'Date': self.date,
            'Ratings': self.ratings,
            'Overall Rating': self.get_overall_rating(),
            'Review': self.review
        }

# Create the tables
Base.metadata.create_all(engine)

# Set up the session to interact with the database
Session = sessionmaker(bind=engine)
