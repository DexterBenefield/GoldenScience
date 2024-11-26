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
    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id')) #

    # Establish a relationship back to the User class
    user = relationship('User', back_populates='ratings')

# Set up the SQLite database
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Example usage: Add a user and a rating
new_user = User(name='Alice')
session.add(new_user)
session.commit()

new_rating = Rating(value=5, user_id=new_user.id)
session.add(new_rating)
session.commit()

# Query the database
for rating in session.query(Rating).all():
    print(f'User {rating.user.name} gave a rating of {rating.value}')