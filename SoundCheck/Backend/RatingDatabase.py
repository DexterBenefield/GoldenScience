from sqlalchemy import create_engine, Column, Integer, String, JSON, PickleType, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError
from datetime import datetime

Base = declarative_base()

# Define the User class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Establish a relationship to the Rating class
    ratings = relationship('Rating', back_populates='user')

# Define the Rating class
class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Link to the User model
    review_text = Column(String, nullable=False)
    location_rating = Column(Integer, nullable=False)
    parking_rating = Column(Integer, nullable=False)
    merch_rating = Column(Integer, nullable=False)
    sound_quality_rating = Column(Integer, nullable=False)
    set_list_rating = Column(Integer, nullable=False)
    ticket_price_rating = Column(Integer, nullable=False)
    facilities_rating = Column(Integer, nullable=False)
    security_rating = Column(Integer, nullable=False)
    average_rating = Column(Float, nullable=False)
    # Establish a relationship back to the User class
    user = relationship('User', back_populates='ratings')





ratingEngine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(ratingEngine)

# # Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

# # Example usage: Add a user and a rating
# new_user = User(name='Alice')
# session.add(new_user)
# session.commit()

# new_rating = Rating(value=5, user_id=new_user.id)
# session.add(new_rating)
# session.commit()

# # Query the database
# for rating in session.query(Rating).all():
#     print(f'User {rating.user.name} gave a rating of {rating.value}')