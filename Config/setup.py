import sqlite3

def buildTable(strQuery):
    conn = sqlite3.connect('moymgmt.db')
    cursor = conn.cursor()
    cursor.execute(strQuery)
    conn.commit()
    conn.close()
    print("# Build done")


if __name__=="__main__":
    print("build table User...")
    strQuery = """CREATE TABLE users (id INTEGER PRIMARY KEY,username TEXT NOT NULL,password TEXT,lastlogin date)"""
    buildTable(strQuery)
