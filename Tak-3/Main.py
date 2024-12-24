users = {}
books = {}
def data():
    global users, books

    f = open("usersinfo.txt", "r", encoding="utf-8")
    for line in f:
        data = line.strip().split(",")
        if len(data) >= 3: 
            username = data[0] 
            password = data[1]  
            borrowed_count = int(data[2]) 
            if len(data) > 3:
                borrowed_books = data[3:]  
            else:
                borrowed_books = [] 
            
            users[username] = {
                "password": password,
                "borrowed_count": borrowed_count,
                "borrowed_books": borrowed_books
            }
        else:
            print(f"Error: Invalid data format in line: {line}")
    f.close() 

    f = open("books.txt", "r", encoding="utf-8")
    for line in f:
        data = line.strip().split(",")
        if len(data) == 4:  
            isbn = data[0]  
            title = data[1] 
            author = data[2]  
            count = int(data[3]) 
            books[isbn] = {
                "title": title,
                "author": author,
                "count": count
            }
        else:
            print(f"Error: Invalid data format in line: {line}")
    f.close()

def saveData():
    global users, books
    f = open("usersinfo.txt", "w", encoding="utf-8")
    for username, user_data in users.items():
        line = f"{username},{user_data['password']},{user_data['borrowed_count']}"
        if user_data["borrowed_books"]:
            line += "," + ",".join(user_data["borrowed_books"])
        f.write(line + "\n")
    f.close()  
    
    f = open("books.txt", "w", encoding="utf-8")
    for isbn, book_data in books.items():
        line = f"{isbn},{book_data['title']},{book_data['author']},{book_data['count']}"
        f.write(line + "\n")
    f.close()  

def login():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    if username in users and users[username]["password"] == password:
        print(f"Welcome {username}!")
        menu(username)
    else:
        print("Invalid username or password. Please try again.")

def add():
    isbn = input("Enter ISBN: ").strip()
    if isbn in books:
        print("This book already exists!")
        return
    title = input("Enter Title: ").strip()
    author = input("Enter Author: ").strip()

    while True:
        try:
            count = int(input("Enter Number of Copies: ").strip())
            if count < 0:
                print("Count cannot be negative. Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

    books[isbn] = {"title": title, "author": author, "count": count}
    print("Book added successfully!")


def remove():
    isbn = input("Enter ISBN of the book to remove: ").strip()
    if isbn not in books:
        print("Book not found!")
        return
    for user in users.values():
        if isbn in user["borrowed_books"]:
            user["borrowed_books"].remove(isbn)
            user["borrowed_count"] -= 1
    del books[isbn]
    print("Book removed successfully!")

def search():
    query = input("Enter book title or author to search: ").strip().lower()
    found = False
    for book in books.values():
        if query in book["title"].lower() or query in book["author"].lower():
            print(f"Title: {book['title']}, Author: {book['author']}, Copies: {book['count']}")
            found = True
    if not found:
        print("No books found matching your search.")

def borrow(username):
    if users[username]["borrowed_count"] >= 3:
        print("You have already borrowed the maximum number of books!")
        return
    isbn = input("Enter ISBN of the book to borrow: ").strip()
    if isbn not in books or books[isbn]["count"] == 0:
        print("Book not available!")
        return
    users[username]["borrowed_books"].append(isbn)
    users[username]["borrowed_count"] += 1
    books[isbn]["count"] -= 1
    print("Book borrowed successfully!")

def returnBook(username):
    isbn = input("Enter ISBN of the book to return: ").strip()
    if isbn not in users[username]["borrowed_books"]:
        print("You have not borrowed this book!")
        return
    users[username]["borrowed_books"].remove(isbn)
    users[username]["borrowed_count"] -= 1
    books[isbn]["count"] += 1
    print("Book returned successfully!")

def show(username):
    if not users[username]["borrowed_books"]:
        print("You have not borrowed any books.")
        return
    print("Books you have borrowed:")
    for isbn in users[username]["borrowed_books"]:
        print(f"- {books[isbn]['title']} by {books[isbn]['author']}")

def menu(username):
    while True:
        print("""
        Main Menu:
        1. Insert New Book
        2. Delete Book
        3. Search 
        4. Borrow Book
        5. Return Book
        6. Report of Borrowed Books
        7. Update Files
        8. Logout
        """)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add()
        elif choice == "2":
            remove()
        elif choice == "3":
            search()
        elif choice == "4":
            borrow_book(username)
        elif choice == "5":
            returnBook(username)
        elif choice == "6":
            show(username)
        elif choice == "7":
            saveData()
            print("Data saved successfully!")
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    data()
    while True:
        print("""
        Welcome to the Library Management System:
        1. Login
        2. Exit
        """)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            login()
        elif choice == "2":
            saveData()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
