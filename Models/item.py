from Models.dbmanager import setData,fetchData
from datetime import datetime

class Ticket:
    def __init__(self,id):
        self.id = id
    
    def createTicket(self):
        pass

class Item(Ticket):
    
    def __init__(self,name,price,quantity,region,currency):
        super().__init__("44181")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.createdAt = datetime.now()
        self.ticket = super().id
        self.region = region
        self.currency = currency
    
    def saveItem(self):
        pass