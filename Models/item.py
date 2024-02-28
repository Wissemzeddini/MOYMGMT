from Models.dbmanager import setData,fetchData
from datetime import datetime

class Ticket:
    def __init__(self,user):
        self.createdAt = datetime.now()
        self.user = user
        self.code = self.generateTodayTimeStamp()
    
    def createTicket(self):
        query = "insert into `tickets`(createdAt,user,code) values(?,?,?)"
        data = (self.createdAt,self.user,self.code)
        if not self.checkTicketIsExiste():
            try:
                setData(query,data)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            print(f"Ticket {self.code} is duplicated.")
        return self.code

    def generateTodayTimeStamp(self,prefix="TK"):
        return prefix+"-"+str(datetime.now().day)+str(datetime.now().month)+str(datetime.now().year)
    
    def checkTicketIsExiste(self):
        query = "select * from `tickets` where code=? and user=?;"
        data = (self.code, self.user)
        rows = fetchData(query,data)
        if len(rows)==0:
            return False
        return True
    
    def selectTicketID(self):
        query = "select id from `tickets` where code=? limit 1;"
        data = (self.code,)
        rows = fetchData(query,data)
        if len(rows):
            return rows[0][0]
        raise Exception(f"No such Ticket under this code: {self.code}")
    
    def getAllTickets(self):
        query = "select * from `tickets` where user=?;"
        data = (self.user,)
        rows = fetchData(query,data)
        if len(rows):
            return rows
        return ["There is no data to display!"]

class Item(Ticket):
    
    def __init__(self,category,subcategory,name,price,quantity,region,currency,user):
        super().__init__(user)
        super().createTicket()
        self.category = category
        self.subcategory = subcategory
        self.name = name
        self.price = price
        self.quantity = quantity
        self.createdAt = datetime.now()
        self.ticket = super().selectTicketID()
        self.region = region
        self.currency = currency
        self.user = user
    
    def saveItem(self):
        if super().checkTicketIsExiste():
            query = "insert into `items`(category,subcategory,name,current_price,original_price,quantity,ticket,region,currency,user,createdAt) values(?,?,?,?,?,?,?,?,?,?,?)"
            data = (self.category,self.subcategory,self.name,self.price,self.price,self.quantity,self.ticket,self.region,self.currency,self.user,self.createdAt)
            if self.checkItemIfExsist():
                self.updateItemPrice()
                print("Update done successfuly")
            else:
                try:
                    setData(query,data)
                    print("New Item has been added successfuly")
                except Exception as e:
                    print("Error happing during creating new items", str(e))
    
    def checkItemIfExsist(self):
        query = "select * from `items` where category=? and subcategory=? and name=? and original_price=? and ticket=? and user=? limit 1;"
        data = (self.category,self.subcategory,self.name,self.price,self.ticket,self.user)
        rows = fetchData(query,data)
        if len(rows):
            return True
        return False
    
    def updateItemPrice(self):
        query="update `items` set current_price=current_price+?, quantity=quantity+? where category=? and subcategory=? and name=? and ticket=? and user=?;"
        data = (float(self.price),self.quantity,self.category,self.subcategory,self.name,self.ticket,self.user)
        try:
            setData(query,data)
            return True
        except Exception as e:
            print(f"Error when update the item [{self.name}]: ",str(e))
        return False
