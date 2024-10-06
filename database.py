from classes import User
def create_user(cursor,username:str,password:str,first_name:str,role:str="reader"):
    if not check_user(cursor,username):
        cursor.execute(f"""
                INSERT INTO User (username,password,first_name,role)
                VALUES ('{username}','{password}','{first_name}','{role}');
                """)
        return login(cursor,username,password)
    else:
        return False

def create_super_user(cursor,username:str,password:str,first_name:str,role:str="superuser"):
    return create_user(cursor,username,password,first_name,role)

def register_library(cursor,library_name,admin_username):
    if check_user(cursor,admin_username):
        cursor.execute(f"""
                SELECT user_id FROM User
                WHERE username = '{admin_username}'
                       """)
        admin_id = cursor.fetchall()
        cursor.execute(f"""
                INSERT INTO Library (,name,admin)
                VALUES ('{library_name}',{admin_id})
                        """)
    else:
        return "No such admin"

def change_library_admin(cursor):
    cursor.execute(f"""
            SELECT library_id FROM Library 
                   """)
    libraries = cursor.fetchall()
    for library in libraries:
            print(library)

    library_id = input("Choose a library (only id): ")
    new_admin_username = input("Write new admin's username: ")
    if check_user(cursor,new_admin_username):
        cursor.execute(f"""
                SELECT user_id FROM User
                WHERE username = '{new_admin_username}'
                       """)
        admin_id = cursor.fetchall()
        cursor.execute(f"""
                UPDATE Library
                SET admin = {admin_id}
                WHERE library_id = {library_id}
                       """)
        return "Changed"
    else:
            print("There is no such admin")
            option = input('1: Register new admin\n2: Do not change old admin\n')
            if option == '1':
                User.register_admin(cursor)
                change_library_admin(cursor)
            if option == '2':
                return 'Admin is not changed'
            
def check_user(cursor,username,password=None):
    if not password:
        cursor.execute(f"""
            SELECT * FROM User 
            WHERE username = '{username}';
        """)
    else:
        cursor.execute(f"""
            SELECT * FROM User 
            WHERE username = '{username}' AND password = '{password}';
        """)
    return cursor.fetchone()

def login(cursor,username,password):
    user = check_user(cursor,username,password)
    return user

def add_book(cursor,name,author,genre,year,count):
    cursor.execute(f"""
            SELECT library_id FROM Library 
                   """)
    libraries = cursor.fetchall()
    for library in libraries:
            print(library)

    library_id = input("Choose a library (only id): ")
    if not find_book(cursor,int(library_id),name):
        cursor.execute(f"""
                SELECT MAX(book_id) FROM Book
                       """)
        last_book_id = cursor.fetchall()
        cursor.execute(f"""
                       INSERT INTO Book (book_id,name,librarry,author,genre,year,quantity)
                       VALUES ({last_book_id+1},'{name}',{int(library_id)},'{author}','{genre}',{year},{count})
                        """)
    else:
        return "There is already such book"

def find_book(cursor,library_id,book_name):
    cursor.execute(f"""
            SELECT * FROM Book
            WHERE librarry = {library_id} AND name = {book_name}
                    """)
    book_data = cursor.fetchall()
    return book_data

def increase_count(cursor,book_id):
    cursor.execute(f"""
            SELECT quantity FROM Book
            WHERE book_id = {book_id}
                   """)
    count = cursor.fetchall()
    cursor.execute(f"""
            UPDATE Book
            SET quantity = {count + 1}
                   """)

def decrease_count(cursor,book_id):
    cursor.execute(f"""
            SELECT quantity FROM Book
            WHERE book_id = {book_id}
                   """)
    count = cursor.fetchall()
    cursor.execute(f"""
            UPDATE Book
            SET quantity = {count - 1}
                   """)

def rent_book(cursor,user_id,book_id,date,library_id,status="Rented"):
    cursor.execute(f"""
            INSERT INTO Rented_book (reader,book,date,library,status)
            VALUES ({user_id},{book_id},'{date}',{library_id},'{status}')
                   """)
    decrease_count(cursor,book_id)

def check_user_rented_books(cursor,user_id,library_id):
    cursor.execute(f"""
            SELECT * FROM Rented_book
            WHERE reader = {user_id} AND library = {library_id}
                   """)
    all_rented_books = cursor.fetchall()
    if len(all_rented_books) > 3:
        return False
    else:
        return True
    
def return_book(cursor, user_id,library_id,book_id):
    cursor.execute(f"""
            UPDATE Rented_book
            SET status = "Returned"
            WHERE reader = {user_id} AND library = {library_id} AND book = {book_id}
                   """)
    increase_count(cursor,book_id)
    
