from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Concert import Base

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    concert_id = Column(Integer, ForeignKey('concerts.id'))
    review_text = Column(String)
    rating = Column(Float)
    user = relationship("UserProfile")
    concert = relationship("Concert")