from argon2 import PasswordHasher
import uuid
import json
import requests
import mysql.connector
import numpy as np

ph = PasswordHasher()


##TEMP##
serverUrl = "http://localhost:5000"
##TEMP##

'''
with open("data.json", "r") as dataFile:
    appData = json.load(dataFile)
'''

class Account():
    def __init__(self, accountName, rootPw):
        url = serverUrl + "/register"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountname": accountName, "rootpwhash": ph.hash(rootPw)}

        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            print("Registered!")
            self.accountId = response["accountid"]

    def __init__(self, id):
        self.id = id

        db = mysql.connector.connect(host="iron-pickaxe.pootislocal.net", user="paranoiadev", password="devpwd", database="apar", buffered = True)
        dbcursor = db.cursor()

        sqlcmd = "SELECT * FROM accounts WHERE accountid = %s"
        value = (self.id, )
        dbcursor.execute(sqlcmd, value)
        dbaccount = dbcursor.fetchone()
        if dbaccount is None:
            print("Account not in database!")
            return False
        self.balance = dbaccount[1]

        sqlcmd = "SELECT * FROM users WHERE accountid = %s"
        dbcursor.execute(sqlcmd, value)
        users = dbcursor.fetchall()


    
    def changeBalance(self, amount):
        self.balance += amount

class User(Account):
    def __init__(self, username, passwordIn):
        self.username = username

class Transaction(Account):
    def __init__(self, user, amount):
        self.amount = amount
        self.owner = user
        self.id = str(uuid.uuid4())
    
    def commit(self):
        super().changeBalance(amount)

bruh = Account(accountName="test", rootPw="hehe")