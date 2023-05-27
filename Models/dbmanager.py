import sqlite3

def buildQuery(strQuery,data):
    conn = sqlite3.connect('moymgmt.db')
    cursor = conn.cursor()
    cursor.execute(strQuery,data)
    conn.commit()
    conn.close()
    print("# query executed successfuly")

def fetchQuery(strQuery,data):
    conn = sqlite3.connect('moymgmt.db')
    cursor = conn.cursor()
    cursor.execute(strQuery,data)
    rows = cursor.fetchall()
    conn.close()
    return rows