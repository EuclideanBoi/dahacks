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
        self.currentUser = None
        self.currentPassword = None
    
    def registerAccount(self, rootPw):
        url = serverUrl + "/register"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountname": self.accountName, "rootpwhash": ph.hash(rootPw)}

        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            self.accountId = response.json()["accountid"]
            self.accountInitialized = True
            print("Registered account " + self.accountId)
            return True
        return False

    def getExisting(self):
        url = serverUrl + "/getaccount"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountname": self.accountName}
        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            self.accountInitialized = True
            self.accountId = response.json()["accountid"]
            print("Got account " + self.accountId)

    def registerUser(self, username, password, rootpw):
        url = serverUrl + "/adduser"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountname": self.accountName, "username": username, "password": ph.hash(password), "rootpw": rootpw}

        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            print("Registered user " + username)
        else:
            print("reg error")

    def useUser(self, username, password):
        if not self.accountInitialized:
            print("Account not initialized!")
            return False

        url = serverUrl + "/login"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountname": self.accountName, "username": username, "password": password}

        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            print("Authenticated")
            self.authenticated = True
            self.currentUser = username
            self.currentPassword = password
            return True
        else:
            print("Auth error!")
            return False
    
    def getTransactions(self):
        if not self.authenticated:
            print("Not authenticated!")
            return None

        url = serverUrl + "/gettransactions"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountid": self.accountId, "username": self.currentUser, "password": self.currentPassword}

        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            balance = response.json()
            return balance
        else:
            print("Error")
            return None

    def newTransaction(self, amount, description):
        if not self.authenticated:
            print("Not authenticated!")
            return False
        
        url = serverUrl + "/transaction"
        headers = {"Content-type": "application/json"}
        jsonData = {"accountid": self.accountId, "username": self.currentUser, "password": self.currentPassword, "amount": amount, "description": description}

        response = requests.post(url, headers=headers, json=jsonData)
        if response.status_code == 200:
            return True
        return False
'''
class User(Account):
    def __init__(self, username, passwordIn):
        self.username = username
'''
'''
class Transaction(Account):
    def __init__(self, user, amount):
        self.amount = amount
        self.owner = user
        self.id = str(uuid.uuid4())
    
    def commit(self):
        super().changeBalance(amount)
'''