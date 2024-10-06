from classes import User,Library,Book,RentBook
from functions import show_libraries
import sqlite3


connection = sqlite3.connect('library.db')
cursor = connection.cursor()

User.create_super_user(cursor)

user = None
menu = None
library = None

while True:

    if not user:
        print("1: Login\n2: Register")
        option = input("Choose an option: ")
        if option == '1':
            user = User.login(cursor)
        else:
            user = User.register(cursor)
    if user:

        if user.user_role == 'superuser':
            print('1: register admin\n2: register Library\n4: Change library admin\n3: Exit')
            menu = input('Choose an option: ')

            if menu == '1':
                res = User.register_admin()
                print(res)

            elif menu == "2":
                res = User.register_library()
                print(res)
            
            elif menu == '4':
                res = User.change_library_admin(show_libraries())

            elif menu == "3":
                user = None

        elif user.user_role == 'admin':
            print('1: add book\n2: Exit')
            menu = input('Choose an option: ')
            if menu == '1':
                # for i in show_libraries():
                #     print(i.admin,user.username)
                libraries = [x for x in show_libraries() if user.username == x.admin.strip()]
                
                for library in libraries:
                    print(library)
                
                library_id = input('Enter library Id: ')

                library = [x for x in libraries if x.id == library_id]
                library[0].add_book()
                

            if menu == '2':
                user = None
                menu = None

        elif user.user_role == 'reader':
            if not menu:
                print('1: See libraries\n2: Log out')
                menu = input('Choose an option: ')
            if menu == '1':
                if not library:
                    libraries = show_libraries()
                    for library in libraries:
                        print(library)
                    library_id = input("Choose a library: ")

                    library = [x for x in libraries if x.id == library_id]
                if library:
                    library[0].read_books()
                    print('1: Find books\n2: Exit')
                    sub_menu = int(input('Choose an option: '))
                    if sub_menu == 1:
                        res = library[0].find_book()
                        if not res:
                            print("Kitob topilmadi")
                        else:
                            for book in res:
                                print(book)
                            print('1: Rent book\n2: Exit')
                            sub_menu = input('choose an option: ')
                            if sub_menu == "1":
                                book_id = input('Kitobni idsini kiriting: ')
                                book = [book for book in res if int(book.id) == int(book_id)]
                                print(book[0])
                                if RentBook.rent_book(user,library[0],book[0]):
                                    print("siz kitobni oldiz ")
                                else:
                                    print("Kitobni olaolmadiz!!! ")

                    if sub_menu == 2:
                        library = None
                        menu = None
            if menu == '2':
                user = None
                menu = None

connection.commit()
connection.close()
