import sqlite3
import logging as log

db_file_path = "DataBase.db"


def login_credentials(username):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        # Execute a query to retrieve data
        query = "select username, password "
        query+= " ,role from people  "
        query+=" where username = ?"
        
        log.warning(query)
        cursor.execute(query,(username,))

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Print the retrieved data
        username=""
        pwd = ""
        role = ""
        for row in rows:
            log.warning(row)
            username = row[0]
            pwd = row[1]
            role = row[2]

    except sqlite3.Error as e:
        print("Error occurred:", e)

    finally:
        if conn:
            conn.close()
            
            
    return username,pwd,role

