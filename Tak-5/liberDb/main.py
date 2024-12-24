import sqlite3
import os

def initialize_database():

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()


    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        borrowed_count INTEGER NOT NULL,
                        borrowed_books TEXT
                    )''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        isbn TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        copies INTEGER NOT NULL
                    )''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS borrows (
                        username TEXT,
                        isbn TEXT,
                        FOREIGN KEY(username) REFERENCES users(username),
                        FOREIGN KEY(isbn) REFERENCES books(isbn)
                    )''')

    conn.commit()
    conn.close()

def populate_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    users_file = open('usersinfo.txt', 'r')
    for line in users_file:
        data = line.strip().split(',')
        username = data[0]
        password = data[1]
        borrowed_count = int(data[2])
        if len(data) > 3:
            borrowed_books = ','.join(data[3:])
        else:
            borrowed_books = None
        cursor.execute('''INSERT OR REPLACE INTO users (username, password, borrowed_count, borrowed_books) 
                           VALUES (?, ?, ?, ?)''', (username, password, borrowed_count, borrowed_books))
    users_file.close()

    books_file = open('books.txt', 'r')
    for line in books_file:
        data = line.strip().split(',')
        isbn = data[0]
        title = data[1]
        author = data[2]
        copies = int(data[3])
        cursor.execute('''INSERT OR REPLACE INTO books (isbn, title, author, copies)  
                           VALUES (?, ?, ?, ?)''', (isbn, title, author, copies))
    books_file.close()

    conn.commit()
    conn.close()

def login():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    while True:
        username = input("Enter Username: ")

        if username.isdigit():
            print("Username must be a string. Please try again.")
            continue

        password = input("Enter Password: ")

        cursor.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
        user = cursor.fetchone()

        if user:
            print(f"Welcome Dear {username}")
            main_menu(username)
            break
        else:
            print("Invalid username or password. Try again.")

    conn.close()

def main_menu(username):
    while True:
        print("\n1. Insert New Book")
        print("2. Delete Book")
        print("3. Search")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Report of Borrowed Books")
        print("7. Update Files")
        print("8. Logout")
        choice = input("Enter Your Choice (1-8): ")

        if choice == '1':
            insert_new_book()
        elif choice == '2':
            delete_book()
        elif choice == '3':
            search_books()
        elif choice == '4':
            borrow_book(username)
        elif choice == '5':
            return_book(username)
        elif choice == '6':
            report_borrowed_books(username)
        elif choice == '7':
            update_files()
        elif choice == '8':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def insert_new_book():
    import sqlite3
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    try:
        isbn = input("Enter ISBN: ")
        # if not isbn.isdigit():
        #     raise ValueError("ISBN must be a numeric value.")

        title = input("Enter Title: ")
        if not title.isalpha():
            raise ValueError("Title must only contain letters.")

        author = input("Enter Author: ")
        if not author.isalpha():
            raise ValueError("Author must only contain letters.")

        copies = input("Enter Number of Copies: ")
        if not copies.isdigit():
            raise ValueError("Number of copies must be a numeric value.")
        copies = int(copies)


        cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        existing_book = cursor.fetchone()
        if existing_book:
            print("This book already exists in the library. Book not added.")
        else:

            cursor.execute('''INSERT INTO books (isbn, title, author, copies) VALUES (?, ?, ?, ?)''',
                           (isbn, title, author, copies))
            conn.commit()
            print("Book inserted successfully.")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except sqlite3.IntegrityError:
        print("ISBN already exists. Book not added.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def delete_book():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    try:
        isbn = input("Enter ISBN of the book to delete: ")


        cursor.execute('''SELECT * FROM books WHERE isbn = ?''', (isbn,))
        book = cursor.fetchone()

        if book:

            cursor.execute('''DELETE FROM books WHERE isbn = ?''', (isbn,))

            cursor.execute('''DELETE FROM borrows WHERE isbn = ?''', (isbn,))


            cursor.execute('''SELECT username, borrowed_books FROM users WHERE borrowed_books LIKE ?''', (f"%{isbn}%",))
            users_with_book = cursor.fetchall()

            for username, borrowed_books in users_with_book:
                if borrowed_books:

                    borrowed_list = borrowed_books.split(',')
                    if isbn in borrowed_list:
                        borrowed_list.remove(isbn)
                        updated_books = ','.join(borrowed_list)


                        cursor.execute('''UPDATE users 
                                          SET borrowed_count = borrowed_count - 1, 
                                              borrowed_books = ? 
                                          WHERE username = ?''', (updated_books, username))

            conn.commit()
            print("Book and related records deleted successfully.")
        else:
            print("Book not found in the library.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def search_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    query = input("Enter a keyword to search: ")

    cursor.execute('''SELECT * FROM books WHERE title LIKE ? OR author LIKE ?''',
                   (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()

    if results:
        for book in results:
            print(book)
    else:
        print("No books found.")

    conn.close()

def borrow_book(username):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    try:
        isbn = input("Enter ISBN to borrow: ")
        cursor.execute('''SELECT * FROM books WHERE isbn = ?''', (isbn,))
        book = cursor.fetchone()

        if book and book[3] > 0:
            cursor.execute('''SELECT borrowed_count, borrowed_books FROM users WHERE username = ?''', (username,))
            user_data = cursor.fetchone()
            borrowed_count = user_data[0]
            if user_data[1]:
                borrowed_books = user_data[1].split(',')
            else:
                borrowed_books = []

            if isbn in borrowed_books:
                print("You have already borrowed this book.")
            elif borrowed_count < 3:
                cursor.execute('''UPDATE books SET copies = copies - 1 WHERE isbn = ?''', (isbn,))
                cursor.execute('''UPDATE users SET borrowed_count = borrowed_count + 1, 
                                  borrowed_books = ? WHERE username = ?''',
                               (','.join(borrowed_books + [isbn]), username))
                cursor.execute('''INSERT INTO borrows (username, isbn) VALUES (?, ?)''', (username, isbn))
                conn.commit()
                print("Book borrowed successfully.")
            else:
                print("You cannot borrow more than 3 books.")
        else:
            print("Book not available.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def return_book(username):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    try:
        isbn = input("Enter ISBN to return: ")


        cursor.execute('''SELECT * FROM borrows WHERE username = ? AND isbn = ?''', (username, isbn))
        borrow_record = cursor.fetchone()

        if not borrow_record:
            print("You have not borrowed this book or the ISBN is incorrect.")
            return


        cursor.execute('''SELECT borrowed_books FROM users WHERE username = ?''', (username,))
        user_data = cursor.fetchone()
        if user_data[0]:
            borrowed_books = user_data[0].split(',')
        else:
            borrowed_books = []

        if isbn in borrowed_books:
            borrowed_books.remove(isbn)
        else:
            print("This book is not in your borrowed list.")
            return


        cursor.execute('''UPDATE books SET copies = copies + 1 WHERE isbn = ?''', (isbn,))


        cursor.execute('''UPDATE users SET borrowed_count = borrowed_count - 1, 
                          borrowed_books = ? WHERE username = ?''',
                       (','.join(borrowed_books) if borrowed_books else None, username))


        cursor.execute('''DELETE FROM borrows WHERE username = ? AND isbn = ?''', (username, isbn))

        conn.commit()
        print("Book returned successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def report_borrowed_books(username):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT b.isbn, b.title FROM borrows br 
                      JOIN books b ON br.isbn = b.isbn 
                      WHERE br.username = ?''', (username,))
    books = cursor.fetchall()

    if books:
        for book in books:
            print(book)
    else:
        print("No borrowed books.")

    conn.close()

def update_files():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()


    users_file = open('usersinfo.txt', 'w')


    cursor.execute('''SELECT * FROM users''')
    users = cursor.fetchall()


    for user in users:
        if user[3]:
            borrowed_books = user[3]
        else:
            borrowed_books = ''
        users_file.write(f"{user[0]},{user[1]},{user[2]},{borrowed_books}\n")

    users_file.close()



    books_file = open('books.txt', 'w')

    cursor.execute('''SELECT * FROM books''')
    books = cursor.fetchall()


    for book in books:
        books_file.write(f"{book[0]},{book[1]},{book[2]},{book[3]}\n")

    books_file.close()

    conn.close()
    print("Files updated successfully.")

def main():
    initialize_database()
    populate_database()

    while True:
        print("\n1. Login")
        print("2. Exit")
        choice = input("Enter Your Choice (1 or 2): ")

        if choice == '1':
            login()
        elif choice == '2':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
