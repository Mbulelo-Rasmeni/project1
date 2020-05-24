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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    """Search for a book by ISBN or Author or Title"""

    # Get form information.
    query = request.form.get("search")
    try:
        # Make sure book exists.
        if db.execute("SELECT * FROM books WHERE isbn = :isbn OR title = :title OR author = :author", {"isbn": query, "title":query, "author":query}).rowcount == 0:
            return render_template("error.html", message="That book or author does not exist.")
        books = db.execute("SELECT * FROM books WHERE isbn = :isbn OR title = :title OR author = :author", {"isbn": query, "title":query, "author":query}).fetchall()
        return render_template("BookSearch.html", books=books)
        db.commit()
    except ValueError:
        return render_template("error.html", message="Book or Author does not exist.")

    return render_template("success.html")

@app.route("/bookDetails/<str:isbn>")
def bookDetails(isbn):
    """Book information"""

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html", message="Book or Author does not exist")

    # Get reviews
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",
                            {"isbn": isbn}).fetchall()
    
    rating = 0
    for review in reviews:
        rating+= review.user_rating

    return render_template("BookDetails.html", book=book, reviews=reviews,rating=rating)

@app.route("/BookDetails", methods=["POST"])
def addReview(isbn):
    """Add a user review"""

    # Get user rating from form.
    userRating = request.form.get("userRating")

    # Check if user has reviewed this book before
    try:
        if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
            return render_template("error.html", message="No such flight with that id.")
        db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
            {"name": name, "flight_id": flight_id})
        db.commit()
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")

    # Make sure flight exists.
    
    return render_template("success.html")
