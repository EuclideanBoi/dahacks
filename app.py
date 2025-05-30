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
    def __init__(self, accountName):
        self.accountName = accountName
        self.accountId = None
        self.accountInitialized = False
        self.authenticated = False
        self.users = []
    
    def registerAccount(self, rootPw):
        url = serverUrl + "/register"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountname": self.accountName, "rootpwhash": ph.hash(rootPw)}

        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            self.accountId = response.json()["accountid"]
            print("Registered account " + self.accountId)

    def getExisting(self):
        url = serverUrl + "/getaccount"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountname": self.accountName}
        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            self.accountId = response.json()["accountid"]
            print("Got account " + self.accountId)

    def registerUser(self, username, password, rootpw):
        url = serverUrl + "/adduser"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountname": self.accountName, "username": username, "password": ph.hash(password), "rootpw": rootpw}

        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            print("Registered user " + username)
    
    def changeBalance(self, amount):
        self.balance += amount
'''
class User(Account):
    def __init__(self, username, passwordIn):
        self.username = username
'''
class Transaction(Account):
    def __init__(self, user, amount):
        self.amount = amount
        self.owner = user
        self.id = str(uuid.uuid4())
    
    def commit(self):
        super().changeBalance(amount)