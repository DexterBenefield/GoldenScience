from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from UserProfile import UserProfile 

# Initialize the database
engine = create_engine('sqlite:///app.db')
Base = declarative_base()

# Individual Post Table
class IndividualPost(Base):
    __tablename__ = 'individual_posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship to UserProfile
    user = relationship("UserProfile", back_populates="individual_posts")

# Public Post Table
class PublicPost(Base):
    __tablename__ = 'public_posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship to UserProfile
    user = relationship("UserProfile", back_populates="public_posts")

# Update UserProfile to reference posts
UserProfile.individual_posts = relationship("IndividualPost", back_populates="user", cascade="all, delete-orphan")
UserProfile.public_posts = relationship("PublicPost", back_populates="user", cascade="all, delete-orphan")

# Create tables
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
