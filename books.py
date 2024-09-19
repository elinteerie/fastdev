from fastapi import FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]



@app.get('/books')
async def view_all_books():
    return BOOKS


@app.get('/books/')
async def read_books_by_category(category: str):
    category_to_filter = category
    if category:
        filtered_books = [book for book in BOOKS if book['category'] == category_to_filter]

        return  filtered_books
    
@app.get('/books/{category}')
async def read_books_by_category(category: str):
    category_to_filter = category
    if category:
        filtered_books = [book for book in BOOKS if book['category'] == category_to_filter]

        return  filtered_books