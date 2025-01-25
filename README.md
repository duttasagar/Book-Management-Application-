# Book-Management-Application-
Book Management Application: This application, built with FastAPI and MongoDB, allows users to manage books in an online bookstore. Features include adding, updating, and deleting books, searching for books, and viewing book details. FastAPI ensures fast, efficient handling of requests, with pagination for displaying book listings in the frontend.
# Key Features:
•	View all books: List of all books with pagination.
•	Add new book: A form to add new book records.
•	Edit book: Edit book details.
•	Delete book: Delete a book from the collection.
•	Search books: Search for books by title, author, or genre.
•	Book details: View detailed information about a specific book.
# Prerequisites
Before running the application, ensure you have the following prerequisites:
•	Python 3.7+
•	MongoDB Atlas Account (for MongoDB as the database).
•	pip (Python's package manager
# Installation Instructions
Follow the steps below to set up the environment and run the application.
Step 1: Install Required Packages
Install the required dependencies using pip:
pip install fastapi uvicorn motor jinja2 pydantic
Step 2: Set Up MongoDB
•	Create a MongoDB Atlas account if you don’t have one already: https://www.mongodb.com/cloud/atlas
•	Create a new database cluster and get the Connection String.
•	Replace the connection string in the code with your actual MongoDB Atlas connection string:
python
Copy
uri = "mongodb+srv://username:password@cluster-address.mongodb.net/?retryWrites=true&w=majority&appName=Bookapp"
Make sure your database name is todo_db and the collection is book_store.
Step 3: Run the Application
Now you can run the application using Uvicorn.
uvicorn main:app --reload
•	This will run the FastAPI application on http://127.0.0.1:8000.
•	The --reload flag enables automatic reloading during development.
# API Endpoints
Here is a list of the main API endpoints provided by the application:
1. GET /api/books
  •	Description: Fetches and displays a list of books.
  •	Response: Returns an HTML page with a list of books.
  •	Template: home.html
2. POST /api/books
  •	Description: Adds a new book to the collection.
  •	Request Body: Form data containing book details (title, author, isbn, price, quantity, published_date,   genre, description, last_updated_timestamp, created_timestamp).
  •	Response: Redirects to /api/books and displays the updated list of books.
3. POST /api/books/{data_id}
  •	Description: Deletes a book by its ID.
  •	Request Parameter: data_id (The book ID to delete).
  •	Response: Redirects to /api/books.
4. GET /api/edit/{book_id}
  •	Description: Displays the edit form for a book.
  •	Request Parameter: book_id (The ID of the book to edit).
  •	Response: Returns an HTML page with a form to edit the book's details.
5. POST /api/update/{book_id}
  •	Description: Updates the details of an existing book.
  •	Request Parameters: book_id, along with form data containing updated book details.
  •	Response: Redirects to /api/books.
6. POST /api/search/
  •	Description: Searches for books based on a query (title, author, or genre).
  •	Request Body: Form data containing the search_query.
  •	Response: Returns an HTML page with the search results.
7. GET /api/book_detail/{book_id}
  •	Description: Displays the details of a specific book.
  •	Request Parameter: book_id (The ID of the book).
  •	Response: Returns an HTML page with the book details.
# Templates
  The application uses Jinja2 Templates to render HTML views. The templates are located in the templates directory and are used to render responses for the following pages:
  •	home.html: Displays the list of books.
  •	edit.html: Displays the form to edit a book.
  •	index.html: Displays search results.
  •	book_detail.html: Displays the details of a specific book.
# Error Handling
  The application handles errors using FastAPI’s HTTPException. It handles common errors such as:
  •	Invalid book ID format.
  •	Book not found.
  •	General server errors.
# Testing the Application
  Once the application is running, you can:
  1.	Add a new book via the /api/books form.
  2.	View all books by navigating to /api/books.
  3.	Edit a book by navigating to /api/edit/{book_id}.
  4.	Search for books using the /api/search/ endpoint.
  5.	Delete a book by sending a POST request to /api/books/{data_id}.
