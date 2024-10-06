def show_libraries(cursor):
    cursor.execute(f"""
            SELECT library_id FROM Library 
                   """)
    libraries = cursor.fetchall()
    for library in libraries:
            print(library)


