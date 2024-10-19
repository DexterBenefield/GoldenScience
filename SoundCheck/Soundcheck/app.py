from flask import Flask, render_template
from views2 import views

app = Flask(__name__)

# Home route serving the login page
@app.route("/")
def home():
    return render_template("index.html")

# Sign up route
@app.route("/signup")
def signup():
    return "<h1>Sign Up Page</h1>"

# Log in route
@app.route("/login")
def login():
    return "<h1>Log In Page</h1>"

if __name__ == '__main__':
    app.run(debug=True, port=8000)