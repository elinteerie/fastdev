from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author =author
        self.description = description
        self.rating = rating
        self.published_date=published_date




BOOKS = [
    Book(1, "computer Science", "Coding with Roby", "Very Nice Book", 5, 2020),
    Book(2, "Be Fast with FastAPI", "Ugo", "Very Nice Book", 5, 2022),
    Book(3, "Master Endpoint", "Joshua", "Very Nice Book", 5, 2020), 
    Book(4, "Women Entrepreneurs", "Pjillip", "Very Nice Book", 2, 2012),
    Book(5, "Men Billionaires", "CJohn Ake", "Very Nice Book", 3,2021),
    Book(6, "Reading with Methodology", "Bassey Emma", "Very Nice Book", 1, 2022),
]

@app.get('/books', status_code=200)
async def read_all_books():
    return BOOKS

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not need on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(default=2010, gt=2000, lt=2025)

    model_config ={
        "json_schema_extra": {
            "example": {
                "title": "New Book",
                "author": "John Doe",
                "description": "Description of a New Book",
                "rating": 4,
                'published_date': 2020
            }
        }
    }

@app.post('/create-book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    book = BOOKS.append(find_book_id(new_book))
    return new_book


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) ==0 else BOOKS[-1].id +1

    return book



@app.get('/books{book_id}')
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:

            return book
        


@app.get('/book/')
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return



@app.put('/books/update_book')
async def update_book(book: BookRequest):
    pass


