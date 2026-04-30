from flask import Flask, render_template, request, redirect, url_for
from mongita import MongitaClientDisk
import os
import json

app = Flask(__name__)

# Mongita Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = MongitaClientDisk(os.path.join(BASE_DIR, "mongita_data"))

db = client.bookstore
categories_col = db.category
books_col = db.book

# Populate Data

def populate_data():
    # Reset collections
    categories_col.delete_many({})
    books_col.delete_many({})

    # CATEGORIES
    categories_col.insert_many([
        {"categoryId": 1, "categoryName": "Jet Age Histories"},
        {"categoryId": 2, "categoryName": "Airline Design and Branding"},
        {"categoryId": 3, "categoryName": "Airliner Technology"},
        {"categoryId": 4, "categoryName": "Airline Industry and Operations"}
    ])

    # BOOKS
    books_col.insert_many([
        {
            "bookId": 1,
            "categoryId": 1,
            "categoryName": "Jet Age Histories",
            "title": "747: Creating the World's First Jumbo Jet and Other Adventures from a Life in Aviation",
            "author": "Joe Sutter, Jay Spenser",
            "isbn": "9780062011527",
            "price": 19.99,
            "image": "747-joe-sutter.jpg",
            "readNow": 1
        },
        {
            "bookId": 2,
            "categoryId": 1,
            "categoryName": "Jet Age Histories",
            "title": "Jet Age: The Comet, the 707, and the Race to Shrink the World",
            "author": "Sam Howe Verhovek",
            "isbn": "9781583334362",
            "price": 18.00,
            "image": "jet-age-comet-707.jpg",
            "readNow": 1
        },
        {
            "bookId": 3,
            "categoryId": 1,
            "categoryName": "Jet Age Histories",
            "title": "Come Fly the World: The Jet-Age Story of the Women of Pan Am",
            "author": "Julia Cooke",
            "isbn": "9780358251408",
            "price": 21.99,
            "image": "come-fly-the-world.jpg",
            "readNow": 0
        },
        {
            "bookId": 4,
            "categoryId": 2,
            "categoryName": "Airline Design and Branding",
            "title": "Airline: Style at 30,000 Feet",
            "author": "Keith Lovegrove",
            "isbn": "9781780673165",
            "price": 17.99,
            "image": "airline-style-30000-feet.jpg",
            "readNow": 1
        },
        {
            "bookId": 5,
            "categoryId": 2,
            "categoryName": "Airline Design and Branding",
            "title": "Airline Maps: A Century of Art and Design",
            "author": "Mark Ovenden, Maxwell Roberts",
            "isbn": "9780141993119",
            "price": 26.00,
            "image": "airline-maps.jpg",
            "readNow": 0
        },
        {
            "bookId": 6,
            "categoryId": 2,
            "categoryName": "Airline Design and Branding",
            "title": "Airline Visual Identity: 1945-1975",
            "author": "Matthias Hühne",
            "isbn": "9783981655001",
            "price": 68.00,
            "image": "airline-visual-identity.jpg",
            "readNow": 0
        },
        {
            "bookId": 7,
            "categoryId": 3,
            "categoryName": "Airliner Technology",
            "title": "Supersonic: The Design and Lifestyle of Concorde",
            "author": "Lawrence Azerrad",
            "isbn": "9783791384092",
            "price": 27.50,
            "image": "supersonic-concorde.jpg",
            "readNow": 1
        },
        {
            "bookId": 8,
            "categoryId": 3,
            "categoryName": "Airliner Technology",
            "title": "Boeing 787 Dreamliner",
            "author": "Guy Norris, Mark Wagner",
            "isbn": "9781616732271",
            "price": 24.99,
            "image": "boeing-787-dreamliner.jpg",
            "readNow": 1
        },
        {
            "bookId": 9,
            "categoryId": 3,
            "categoryName": "Airliner Technology",
            "title": "Airbus A380",
            "author": "Robert Jackson, Glen Ashley",
            "isbn": "9781526774095",
            "price": 22.95,
            "image": "airbus-a380.jpg",
            "readNow": 0
        },
        {
            "bookId": 10,
            "categoryId": 4,
            "categoryName": "Airline Industry and Operations",
            "title": "The Airline Business in the Twenty-first Century",
            "author": "Rigas Doganis",
            "isbn": "9780415208833",
            "price": 39.99,
            "image": "airline-business-twenty-first-century.jpg",
            "readNow": 1
        },
        {
            "bookId": 11,
            "categoryId": 4,
            "categoryName": "Airline Industry and Operations",
            "title": "Flying Off Course: The Economics of International Airlines",
            "author": "Rigas Doganis",
            "isbn": "9780203995266",
            "price": 44.99,
            "image": "flying-off-course.jpg",
            "readNow": 0
        },
        {
            "bookId": 12,
            "categoryId": 4,
            "categoryName": "Airline Industry and Operations",
            "title": "Air Transport: A Tourism Perspective",
            "author": "Anne Graham, Frederic Dobruszkes",
            "isbn": "9780128128572",
            "price": 54.99,
            "image": "air-transport-tourism-perspective.jpg",
            "readNow": 0
        }
    ])


# Helper Functions
def strip_mongita_id(document):
    if document and "_id" in document:
        document = dict(document)
        document.pop("_id", None)
    return document


def clean_documents(documents):
    return [strip_mongita_id(doc) for doc in documents]


def get_categories():
    categories = clean_documents(list(categories_col.find()))
    return sorted(categories, key=lambda c: c["categoryName"])


def get_books():
    books = clean_documents(list(books_col.find()))
    return sorted(books, key=lambda b: b["title"])


def get_next_book_id():
    books = list(books_col.find())

    if not books:
        return 1

    return max(book["bookId"] for book in books) + 1


def get_category_name(category_id):
    category = categories_col.find_one({"categoryId": category_id})

    if category:
        return category["categoryName"]

    return ""


def export_json_files():
    categories = get_categories()
    books = get_books()

    with open(os.path.join(BASE_DIR, "categories.json"), "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)

    with open(os.path.join(BASE_DIR, "books.json"), "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)


# Seed database when app starts
populate_data()
export_json_files()


# ROUTE: WORKING HOMEPAGE
# /
@app.route("/", methods=["GET"])
def home():
    categories = get_categories()

    return render_template(
        "index.html",
        categories=categories
    )

# ROUTE: LIST ALL BOOKS
# /read or /read?categoryId=1
@app.route("/read", methods=["GET"])
def read():
    categories = get_categories()
    category_id = request.args.get("categoryId", type=int)

    if category_id is not None:
        selected_category = categories_col.find_one({"categoryId": category_id})

        if not selected_category:
            return render_template(
                "error.html",
                error="Category not found."
            ), 404

        books = clean_documents(list(books_col.find({"categoryId": category_id})))
        books = sorted(books, key=lambda b: b["title"])
        selected_category = strip_mongita_id(selected_category)

    else:
        books = get_books()
        selected_category = None

    return render_template(
        "read.html",
        categories=categories,
        books=books,
        selectedCategory=selected_category
    )

# ROUTE: SHOW CREATE FORM
# /create
@app.route("/create", methods=["GET"])
def create():
    categories = get_categories()

    return render_template(
        "create.html",
        categories=categories
    )

# ROUTE: Insert Book
# /create_post
@app.route("/create_post", methods=["POST"])
def create_post():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    price = request.form.get("price", type=float)
    category_id = request.form.get("categoryId", type=int)
    image = request.form.get("image", "").strip()
    read_now = request.form.get("readNow", type=int)

    if not title or not author or not isbn or price is None or category_id is None or not image or read_now is None:
        return render_template(
            "error.html",
            error="Please fill in all required fields."
        ), 400

    if price < 0:
        return render_template(
            "error.html",
            error="Price cannot be negative."
        ), 400

    category_name = get_category_name(category_id)

    if not category_name:
        return render_template(
            "error.html",
            error="Invalid category selected."
        ), 400

    existing_book = books_col.find_one({"isbn": isbn})

    if existing_book:
        return render_template(
            "error.html",
            error="A book with this ISBN already exists."
        ), 400

    new_book = {
        "bookId": get_next_book_id(),
        "categoryId": category_id,
        "categoryName": category_name,
        "title": title,
        "author": author,
        "isbn": isbn,
        "price": price,
        "image": image,
        "readNow": read_now
    }

    books_col.insert_one(new_book)
    export_json_files()

    return redirect(url_for("read"))

# ROUTE: SHOW EDIT FORM
# /edit/<id>
@app.route("/edit/<int:id>", methods=["GET"])
def edit(id):
    categories = get_categories()
    book = books_col.find_one({"bookId": id})

    if not book:
        return render_template(
            "error.html",
            error="Book not found."
        ), 404

    book = strip_mongita_id(book)

    return render_template(
        "edit.html",
        categories=categories,
        book=book
    )


# ROUTE: Update Book
# /edit_post/<id>
@app.route("/edit_post/<int:id>", methods=["POST"])
def edit_post(id):
    book = books_col.find_one({"bookId": id})

    if not book:
        return render_template(
            "error.html",
            error="Book not found."
        ), 404

    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    price = request.form.get("price", type=float)
    category_id = request.form.get("categoryId", type=int)
    image = request.form.get("image", "").strip()
    read_now = request.form.get("readNow", type=int)

    if not title or not author or not isbn or price is None or category_id is None or not image or read_now is None:
        return render_template(
            "error.html",
            error="Please fill in all required fields."
        ), 400

    if price < 0:
        return render_template(
            "error.html",
            error="Price cannot be negative."
        ), 400

    category_name = get_category_name(category_id)

    if not category_name:
        return render_template(
            "error.html",
            error="Invalid category selected."
        ), 400

    same_isbn_books = list(books_col.find({"isbn": isbn}))

    for same_isbn_book in same_isbn_books:
        if same_isbn_book["bookId"] != id:
            return render_template(
                "error.html",
                error="Another book with this ISBN already exists."
            ), 400

    updated_book = {
        "categoryId": category_id,
        "categoryName": category_name,
        "title": title,
        "author": author,
        "isbn": isbn,
        "price": price,
        "image": image,
        "readNow": read_now
    }

    books_col.update_one(
        {"bookId": id},
        {"$set": updated_book}
    )

    export_json_files()

    return redirect(url_for("read"))

# ROUTE: DELETE BOOK
# /delete/<id>
@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    books_col.delete_one({"bookId": id})
    export_json_files()

    return redirect(url_for("read"))

# ERROR HANDLER
@app.errorhandler(Exception)
def handle_error(e):
    return render_template("error.html", error=e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
