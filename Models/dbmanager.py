import sqlite3

def setData(strQuery,data):
    conn = sqlite3.connect('moymgmt_v2.db')
    cursor = conn.cursor()
    cursor.execute(strQuery,data)
    conn.commit()
    conn.close()
    print("# query executed successfuly")

def fetchData(strQuery,data):
    conn = sqlite3.connect('moymgmt_v2.db')
    cursor = conn.cursor()
    cursor.execute(strQuery,data)
    rows = cursor.fetchall()
    conn.close()
    return rows