from fastapi import FastAPI,Form, Body, Request,HTTPException, status,Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime,date
from bson import ObjectId
from pydantic import BaseModel, Field, ValidationError

app = FastAPI()
uri="mongodb+srv://duttasagar39:sagar111@bookapp.sb97q.mongodb.net/?retryWrites=true&w=majority&appName=Bookapp"

client = AsyncIOMotorClient(uri)
db =client.todo_db
collection = db['book_store']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Jinja2 template setup
templates = Jinja2Templates(directory="templates")

class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the book")
    author: str = Field(..., min_length=1, max_length=100, description="The author of the book")
    isbn: str = Field(...,  description="13-digit ISBN number")
    price: float = Field(..., gt=0, description="Price of the book, must be positive")
    quantity: int = Field(..., ge=1, description="Quantity must be at least 1")
    published_date: datetime = Field(..., description="Date when the book was published")
    genre: str = Field(..., min_length=1, max_length=50, description="Genre of the book")
    description: str = Field(None, max_length=500, description="Description of the book")
    last_updated_timestamp: datetime = Field(..., description="Timestamp of the last update")
    created_timestamp: datetime = Field(..., description="Timestamp of the book's creation")


def str_objectid(id: ObjectId) -> str:
    return str(id)

@app.get('/api/books')
async def form(request: Request):

    try:
        books_cursor = collection.find().limit(100)

        books = await books_cursor.to_list(length=100)

        return templates.TemplateResponse("home.html", {"request": request ,"books":books,})
    except Exception :
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")






@app.post('/api/books')
async def create_record(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    published_date: datetime = Body(...),
    genre: str = Form(...),
    description: str = Form(...),
    last_updated_timestamp: datetime = Body(...),
    created_timestamp: datetime = Body(...)):

    book_data = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "price": price,
            "quantity": quantity,
            "published_date": published_date,
            "genre": genre,
            "description": description,
            "last_updated_timestamp": last_updated_timestamp,
            "created_timestamp": created_timestamp,
       }
    try:
        result = await collection.insert_one(book_data)

        new_book = await  collection.find_one({"_id": result.inserted_id})
        print("data inserted successfully")
        books = await collection.find().to_list(100) 

        return templates.TemplateResponse('home.html', {
            "request": request,
            "title": new_book["title"],
            "author": new_book["author"],
            "isbn": new_book["isbn"],
            "price": new_book["price"],
            "quantity": new_book["quantity"],
            "published_date": new_book["published_date"],
            "genre": new_book["genre"],
            "description": new_book["description"],
            "last_updated_timestamp": new_book["last_updated_timestamp"],
            "created_timestamp": new_book["created_timestamp"],
            "books":books,
        }  )

    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request. Please try again later."
        )



@app.post('/api/books/{data_id}')
async def deleteData(data_id:str , request: Request):
    try:
        book_object_id = ObjectId(data_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    result = await collection.delete_one({"_id": book_object_id})
    return Response(status_code=303, headers={"Location":"/api/books"})



@app.get("/api/edit/{book_id}")
async def edit_form(request: Request, book_id: str):
    try:
        book_object_id = ObjectId(book_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    # Fetch the book from the database
    book = await collection.find_one({"_id": book_object_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return templates.TemplateResponse('edit.html', {
        "request": request,
        "book": book
    })



@app.post("/api/update/{book_id}")
async def update_book(
    request: Request,
    book_id: str,
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    published_date: str = Form(...),  
    genre: str = Form(...),
    description: str = Form(...),):
    try:
        book_object_id = ObjectId(book_id)

    except Exception :
        raise HTTPException(status_code=400, detail="Invalid book ID format" )

    # Prepare the updated data
    updated_data = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "price": price,
        "quantity": quantity,
        "published_date": published_date,
        "genre": genre,
        "description": description,
        "last_updated_timestamp": datetime.today()
    }

    result = await collection.update_one(
        {"_id": book_object_id},
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return Response(status_code=303, headers={"Location": "/api/books"})


@app.post("/api/search/")
async def search_books(
    request: Request,
    search_query: str = Form(...),
):
    try:
        query = {"$or": [
            {"title": {"$regex": search_query, "$options": "i"}},
            {"author": {"$regex": search_query, "$options": "i"}},
            {"genre": {"$regex": search_query, "$options": "i"}}
        ]}

        books = await collection.find(query).to_list(100) 

        return templates.TemplateResponse("index.html", {"request": request, "books": books})
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")



def serialize_book(book):
    book['_id'] = str(book['_id'])  
    return book


@app.get('/api/book_detail/{book_id}')
async def book_details(request: Request, book_id: str):
    book = await collection.find_one({"_id": ObjectId(book_id)})
    try:
        if book:
            book = serialize_book(book)  
            return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})
        else:
            return {"error": "Book not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")













































