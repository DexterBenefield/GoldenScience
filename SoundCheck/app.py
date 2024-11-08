
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker
from UserProfile import UserProfile  # Import your UserProfile class
from Concert import Concert
from Concert import engine
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages
Session = sessionmaker(bind=engine)  # Set up your database session

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  
        email = request.form.get("email")  
        
        db_session = Session()
        new_user = UserProfile(username=username, email=email)
        new_user.add_user_profile(db_session)
        db_session.commit()
        
        flash("Sign up successful! Please log in.")
        return redirect(url_for("login"))
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # Check this against hashed password
        
        # Implement logic to check username and password
        # If valid, redirect to a new page; otherwise, flash an error message
        
        return redirect(url_for("home"))  # Change to appropriate route after login
    
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)