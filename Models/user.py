import dbmanager as db
from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.__password = password
    
    def register(self):
        now = datetime.now()
        if self.check():
            raise Exception("Record already exist")
        query = "insert into users(username,password,lastlogin) values (?,?,?)"
        data =(self.username,self.__password,now)
        try:
            db.buildQuery(query,data)
            return True
        except Exception as e:
            print(e)
            return False
    
    def check(self):
        query = "select * from users where username=? and password=? limit 1"
        rows = db.fetchQuery(query,(self.username,self.__password))
        if len(rows)==1:
            return True
        return False
    
    def get(self):
        query =  "select * from users where username=? and password=? limit 1"
        rows = db.fetchQuery(query,(self.username,self.__password))[0]
        return rows[0],rows[1],rows[2],rows[3]

    def login(self):
        now = datetime.now()
        query = f"""update users set lastlogin={now} where username={self.username}"""
        db.buildQuery(query)
    
    def __str__(self) -> str:
        print(f"username:{self.username}, password:{self.__password}")

    