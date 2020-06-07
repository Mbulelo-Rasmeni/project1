import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():

   # if session.get("user") is None:
   #     session["user"] = []

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            # Make sure user exists.
            if db.execute("SELECT * FROM users WHERE email LIKE :email AND password LIKE :password", {"email": email, "password":password}).rowcount == 0:
                return render_template("error.html", message="That user does not exist.")

            session["user"] = email
            return render_template("BookSearch.html", email=email)
            
            
        except ValueError:
            return render_template("error.html", message="User does not exist.")

@app.route("/register",methods=["POST"])
def register():

    if request.method == "POST" and request.form['new_password'] == request.form['new_confirmPassword']:
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        try:
            # Make sure user exists.
            if db.execute("SELECT * FROM users WHERE email LIKE :email AND password LIKE :password", {"email": new_email, "password":new_password}).rowcount == 0:
                name = request.form['new_name']
                db.execute("INSERT INTO users (name, email, password) VALUES (:name, :email, :password)",{"name": name, "email": new_email, "password":new_password})
                db.commit()

            session["user"] = new_email
            return render_template("BookSearch.html", email=new_email)
            
            
        except ValueError:
            return render_template("error.html", message="Error")
    else:
        return render_template("error.html", message="Passwords do not match.")

@app.route("/BookSearch")
def listAll():

    try:
        # show list of all books.
        if db.execute("SELECT * FROM books ").rowcount == 0:
            return render_template("error.html", message="That book or author does not exist.")
        books = db.execute("SELECT * FROM books ").fetchall()
        return render_template("BookSearch.html", books=books)
    except ValueError:
        return render_template("error.html", message="Book or Author does not exist.")

@app.route("/BookDetails/<string:isbn>")
def BookDetails(isbn):

    """Book information"""

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    if book is None:
        return render_template("error.html", message="Book or Author does not exist")
    else:
        # Get reviews
        reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",{"isbn": isbn}).fetchall()

        rating = 10
        count = 5

        
        for review in reviews:
            rating+= review.user_rating
            count=count+1

        avgRating = int(rating/count)


    return render_template("BookDetails.html", book=book, reviews=reviews,rating=avgRating)

@app.route("/review", methods=["POST"])
def addReview():

    #Check if the current user has reviewed the book before
    if "user" in session:
            user = session["user"]
            book_isbn = request.form['isbn']
            checkRating = db.execute("SELECT * FROM reviews WHERE email = :email AND isbn = :isbn", {"email": user, "isbn":book_isbn}).fetchall()
            if checkRating is None:
                userReview = request.form['userReview']
                userRating = int(request.form['userRating'])
                db.execute("INSERT INTO reviews (email, user_review, user_rating, isbn) VALUES (:email, :user_review, :user_rating, :isbn)",{"email": user, "user_review": userReview, "user_rating":userRating, "isbn":book_isbn})
                db.commit()
                
                
            return render_template("BookSearch.html")

@app.route("/search", methods=["POST"])
def search():
    """Search for a book by ISBN or Author or Title"""

    # Get form information.
    if request.method == "POST":
        query = request.form['search']

    try:
        # Make sure book exists.
        if db.execute("SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author", {"isbn": query, "title":query, "author":query}).rowcount == 0:
            return render_template("error.html", message="That book or author does not exist.")
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author", {"isbn": query, "title":query, "author":query}).fetchall()
        return render_template("BookSearch.html", books=books)
    except ValueError:
        return render_template("error.html", message="Book or Author does not exist.")
