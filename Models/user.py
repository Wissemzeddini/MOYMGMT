from Models.dbmanager import setData,fetchData
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, picture, password):
        self.username = username
        self.email = email
        self.picture = picture
        self.__password = password
    
    def register(self):
        now = datetime.now()
        if not self.checkDuplication():
            return False
        hashed_password = generate_password_hash(self.__password)
        query = "insert into users(username,email,password,lastlogin,account_createdAt,picture,isactivated) values (?,?,?,?,?,?,?)"
        data =(self.username,self.email,hashed_password,now,now,self.picture,1)
        try:
            setData(query,data)
            return True
        except Exception as e:
            print(e)
            return False
    
    def checkDuplication(self):
        query = "select * from users where username=? and email=? limit 1;"
        rows = fetchData(query,(self.username,self.email))
        print(rows)
        if len(rows)==0:
            return True
        return False
    
    def authenticate(self):
        status = False
        query = "select * from users where username=?;"
        rows = fetchData(query,(self.username,))
        for row in rows:
            if check_password_hash(row[3],self.__password):
                print("✅✅ password found under username: ",row[1])
                self.updateLastLogin()
                status = True
        return status
    
    def getUser(self):
        query =  "select * from users where username=? limit 1;"
        rows = fetchData(query,(self.username,))[0]
        return rows[0],rows[1],rows[2],rows[6]

    def updateLastLogin(self):
        now = datetime.now()
        query = "update users set lastlogin=? where username=?;"
        data = (now,query)
        try:
            setData(query,data)
        except Exception as e:
            raise Exception(str(e))
    
    def __str__(self) -> str:
        print(f"username:{self.username}, password:{self.__password}")

    def deleteUser(self,username):
        query = "delete from users where username=?;"
        try:
            setData(query,(username,))
            return True
        except Exception as e:
            print(str(e))
            return False


    