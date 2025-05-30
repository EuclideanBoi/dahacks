import app
from app import Account

#bruh = Account(accountName="test", rootPw="hehe") # REGISTER account OBJECT

bruh2 = Account("test") # create account OBJECT (just name)
bruh2.getExisting() # get account info from database and save it locally
# bruh2.registerUser("newuser", "newpwd", "hehe") # register new user using root info
bruh2.useUser("newuser", "newpwd") # use user for transactions
bruh2.newTransaction(42069, "initial balance again and again") # transaction

balanceSheet = bruh2.getTransactions() # returns array of transaction info

for x in balanceSheet:
    print(x)