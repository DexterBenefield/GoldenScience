from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime
from Concert import Base

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    concert_id = Column(Integer, ForeignKey('concerts.id'))
    review_title = Column(String, nullable=True)
    review_text = Column(String)
    rating = Column(Float, nullable=False) 
    additional_ratings = Column(JSON, nullable=True)  
    timestamp = Column(DateTime, default=datetime.utcnow)
    helpful_count = Column(Integer, default=0)

    user = relationship("UserProfile")
    concert = relationship("Concert")

    def add_helpful_vote(self):
        """Increment helpful count when a review is marked as helpful."""
        self.helpful_count += 1

    def set_category_ratings(self, ratings_dict):
        """
        Set additional ratings for specific categories like 'sound', 'venue', etc.
        :param ratings_dict: Dictionary with category ratings (e.g., {'sound': 4, 'venue': 5})
        """
        self.additional_ratings = ratings_dict

    def display_review(self):
        """Returns a dictionary with review details for easy display."""
        return {
            'Review Title': self.review_title,
            'Review Text': self.review_text,
            'Rating': self.rating,
            'Additional Ratings': self.additional_ratings,
            'Helpful Count': self.helpful_count,
            'Timestamp': self.timestamp
        }
