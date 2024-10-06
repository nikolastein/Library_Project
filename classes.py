from datetime import datetime, timedelta

import database

class User:
    super_user_username = 'admin'
    super_user_password = 'pass1'

    def __init__(self,user_id:int, username: str, password: str, first_name: str, user_role='reader'):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.user_role = user_role

    @classmethod
    def create_super_user(cls,cursor):
        return database.create_super_user(cursor,cls.super_user_username,cls.super_user_password,"admin")

    @classmethod
    def register_admin(cls,cursor):
        username = input('Enter admin username: ')
        password = input('Enter user password: ')
        first_name = input("Enter first name: ")
        role = 'admin'
        return database.create_user(cursor,username,password,first_name,role)

    @classmethod
    def register_library(cls,cursor):
        library_name = input("Enter library name: ")
        admin_username = input("Enter library's admin's username: ")
        return database.register_library(cursor,library_name,admin_username)
    
    @classmethod
    def change_library_admin(cls,cursor):
        return database.change_library_admin(cursor)

    @classmethod
    def register(cls,cursor):
        username = input('Enter username: ')
        password = input('Enter user password: ')
        first_name = input("Enter first name: ")
        role = 'reader'
        user = database.create_user(cursor,username,password,first_name,role)
        if user:
            return cls(*list(user))
        else:
            return None
        
    @classmethod
    def login(cls,cursor):
        username = input('Enter username: ')
        password = input('Enter password: ')
        user = database.login(cursor,username,password)
        if user:
            return cls(*list(user))
        else:
            return None

    @classmethod
    def find_user(cls,cursor,username):
        database.check_user(cursor,username)

class Book:
    
    def __init__(self,id,library_id,name,author,gerne,year,count):
        self.id = id
        self.library_id = library_id
        self.name = name
        self.author = author
        self.gerne = gerne
        self.year = year
        self.count = count

    @property
    def is_available(self):
        return self.count > 0

    def increase_count(self,cursor,book_id):
        database.increase_count(cursor,book_id)
  
    def decrease_count(self,cursor,book_id):
        database.decrease_count(cursor,book_id)

    def __str__(self):
        return f"ID: {self.id} Name: {self.name} Author: {self.author} Genre: {self.gerne}"


class Library:
    
    def __init__(self,id,name:str,admin:User):
        self.id = id
        self.name = name
        self.admin = admin
        self.books = list[Book]
        self.readers = list[User]

    def add_book(self,cursor):
        name = input('Enter name: ')
        author = input('Enter author: ')
        gerne = input('Enter gerne: ')
        year = input('Enter year: ')
        count = input('Enter count: ')
        database.add_book(cursor,name,author,gerne,year,count)

    def find_book(self,cursor,book_name):
        cursor.execute(f"""
                SELECT library_id FROM Library 
                   """)
        libraries = cursor.fetchall()
        for library in libraries:
            print(library)

        library_id = input("Choose a library (only id): ")
        database.find_book(cursor,library_id,book_name)

    def __str__(self):
        return f"ID: {self.id} Name: {self.name}"

class RentBook:
    
    def __init__(self,reader:User,library:Library,book:Book,date:datetime):
        self.reader = reader
        self.library = library
        self.book = book
        self.date = date

    @classmethod
    def check_user_rented_books(cls,cursor,user_id,library_id) :
        database.check_user_rented_books(cursor,user_id,library_id)

    @classmethod
    def rent_book(cls,cursor,user_id,book_id,library_id,days:int = 10):
        if cls.check_user_rented_books(cursor,user_id,library_id):
            today = datetime.now().date()
            date = today + timedelta(days=days)
            database.rent_book(cursor,user_id,book_id,str(date),library_id)
        else:
            return "Not avaible or rented books are over limit"

    def check_date(self,cursor,user_id,book_id):
        pass

    def return_book(self,cursor, user_id,library_id,book_id):
        database.return_book(cursor,user_id,library_id,book_id)