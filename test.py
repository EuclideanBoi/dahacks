import app
from app import Account

#bruh = Account(accountName="test", rootPw="hehe")

bruh2 = Account("test")
bruh2.getExisting()
# bruh2.registerUser("newuser", "newpwd", "hehe")
bruh2.useUser("newuser", "newpwd")
bruh2.newTransaction(42069, "initial balance again and again")

balanceSheet = bruh2.getTransactions()

for x in balanceSheet:
    print(x)