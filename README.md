# Project 1

The project is made up of 2 python files, 5 HTML files and a database with 3 tables

Python files:
import.py is the python file that reads books.csv and load(INSERT) all is data into my heroku database.
application.py is the python file where you'll find all the python flask functions and routes of the project

HTML files:
index.html is the home page/login page of the project where users login or register to use the web app
BookSearch.html is the search page where users search for the books they're looking for
BookDetails.html is the page where the details of each book and it's reviews are displayed
layout.html is the page that has the default layout that is used in the error.html page, the page that's loaded when users make an error

Database:
book table contains the isbn, title, author and year that a book was published. All it's data comes from books.csv
users table contains user id(auto incremented by the database), name, email and password
reviews table contains email, review, rating and isbn for each review given to a book by users of the web app
