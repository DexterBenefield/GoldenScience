from UserProfile import UserProfile
from Concert import Concert
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
import pickle

# Database engine and base class
engine = create_engine('sqlite:///app.db')  # SQLite database
Session = sessionmaker(bind=engine)  # Bind the sessionmaker to the engine

def display_user_profiles(user_profiles):
    print("\nUser Profiles Data:")
    print("-" * 50)
    for profile in user_profiles:
        print(f"ID: {profile[0]}")
        print(f"Username: {profile[1]}")
        print(f"Email: {profile[2]}")
        print(f"Location: {profile[3]}")
        print(f"Bio: {profile[4]}")
        print(f"Visibility: {profile[5]}")
        print(f"First Name: {profile[6]}")
        print(f"Last Name: {profile[7]}")

        # Deserialize and format favorite artists and genres
        favorite_artists = deserialize_data(profile[8])
        favorite_genres = deserialize_data(profile[9])
        upcoming_concerts = deserialize_data(profile[10])
        attended_concerts = deserialize_data(profile[11])
        reviews = deserialize_data(profile[12])

        print(f"Favorite Artists: {', '.join(favorite_artists) if favorite_artists else 'None'}")
        print(f"Favorite Genres: {', '.join(f'{key}: {value}' for key, value in favorite_genres.items()) if favorite_genres else 'None'}")
        print(f"Upcoming Concerts: {', '.join(upcoming_concerts) if upcoming_concerts else 'None'}")
        print(f"Attended Concerts: {', '.join(attended_concerts) if attended_concerts else 'None'}")
        print(f"Reviews: {', '.join(reviews) if reviews else 'None'}")
        print("-" * 50)

def deserialize_data(data):
    if data:
        try:
            # Attempt to load the data assuming it's bytes
            return pickle.loads(data) if isinstance(data, (bytes, bytearray)) else eval(data)
        except Exception as e:
            print(f"Error deserializing data: {e}")
            return []
    return []

def display_concert_reviews(concert_reviews):
    print("\nConcert Reviews:")
    print("-" * 50)
    for review in concert_reviews:
        print(f"Artist: {review['Artist']}")
        print(f"Venue: {review['Venue']}")
        print(f"Date: {review['Date']}")
        print(f"Overall Rating: {review['Overall Rating']}")
        print(f"Review: {review['Review']}")
        print(f"Ratings: {review['Ratings']}")
        print("-" * 50)

def main():
    print("Starting the program...")
    db_session = Session()  # Create a new session instance
    print("Session created.")

    username = "christianknight"
    email = "christianknight1@gmail.com"

    existing_user = db_session.query(UserProfile).filter_by(email=email).first()
    if existing_user:
        print("User with this email already exists. Updating profile...")
        user = existing_user
        user.update_profile(new_first_name="Chris", new_last_name="Knight", new_bio="Concert luvvrrr!")
    else:
        print("Creating a new user profile...")
        user = UserProfile(username=username, email=email, location="Brookhaven")
        user.update_profile(new_first_name="Chris", new_last_name="Knight", new_bio="Concert luvvrrr!")
        user.add_user_profile(db_session)
        print("New user profile added.")

    # Add favorite artists and genres
    user.add_favorite_artist("Beyonce")
    user.add_favorite_artist("Partynextdoor")
    user.add_favorite_genre("RnB")
    user.add_favorite_genre("Rap")

    # Add an upcoming concert
    user.add_upcoming_concert("Megan Thee Stallion - 2024-06-10 - The Battery")

    # Create a concert with multiple ratings
    concert = Concert(artist_name="Beyonce", venue="Mercedes Benz", date="2023-08-01")
    concert.add_rating('venue', 5)
    concert.add_rating('sound_quality', 5)
    concert.add_rating('seating', 5)
    concert.add_review("Best concert of my life! I love you, Beyonce!!!")

    # Add the concert to the database
    concert.add_concert(db_session)
    print("Concert added to the database.")

    # Add the concert review to the user's attended concerts
    user.add_review("Beyonce - 2023-08-01 - Mercedes Benz", "Amazing energy!", 5)

    # Commit the changes for the user profile
    db_session.commit()
    print("Changes committed to the database.")

    # Display full profile details
    profile_details = user.display_profile()
    print("User Profile:")
    print(profile_details)

    # Display detailed concert review
    concert_details = concert.display_concert_details()
    print("\nConcert Review:")
    print(concert_details)

    # Close the session
    db_session.close()

    # Query and display all user profiles from the database
    query_database()

def query_database():
    # Connect to the database
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Execute a query to fetch all data from 'user_profiles' table
    cursor.execute("SELECT * FROM user_profiles")

    # Fetch all rows
    rows = cursor.fetchall()

    # Print out each row in a formatted way
    if rows:
        display_user_profiles(rows)
    else:
        print("No data found in user_profiles table.")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()

