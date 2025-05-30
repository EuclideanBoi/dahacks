import app
from app import Account

#bruh = Account(accountName="test", rootPw="hehe")

bruh2 = Account("test")
bruh2.getExisting()
# bruh2.registerUser("newuser", "newpwd", "hehe")
bruh2.useUser("newuser", "newpwd")