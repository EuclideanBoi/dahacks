import app
from app import Account
import random
import pandas
import numpy as np
from sklearn import linear_model
from datetime import datetime

#bruh = Account(accountName="test", rootPw="hehe") # REGISTER account OBJECT
'''
bruh2 = Account("test") # create account OBJECT (just name)
bruh2.getExisting() # get account info from database and save it locally
# bruh2.registerUser("newuser", "newpwd", "hehe") # register new user using root info
bruh2.useUser("newuser", "newpwd") # use user for transactions
# bruh2.newTransaction(42069, "initial balance again and again") # transaction
'''

'''
for i in range(50):
    amount = round(random.random() * 1000 - 200, 2)
    bruh2.newTransaction(amount, "test transaction number " + str(i))
''' # run to use like 5 million years of cpu time


'''
balanceSheet = bruh2.getTransactions() # returns array of transaction info

total = 0.00

for x in balanceSheet:
    total += float(x[3])
    print(x)

print("total: " + str(round(total, 2)))
'''
'''
df = pandas.read_csv("money.csv")

for x in range(len(df)):
    temp = df.at[x, 'Date']
    if len(temp) == 8:
        temp = "0" + temp
    date = datetime.strptime(temp, "%d-%b-%y").timestamp()
    df.at[x, 'Date'] = int(date)

pandas.to_numeric(pandas.Series(df['Amount']))

x = np.array(df['Date'].to_numpy())
y = np.array(df['Amount'].to_numpy())

x = x.reshape(-1, 1)
y = y.reshape(-1, 1)

regr = linear_model.LinearRegression()
regr.fit(x, y)

print(regr.predict([[1530826937]]))
print(regr.predict([[1540826937]]))
'''

datestring = "05/30/2025 13:58:30"
date = datetime.strptime(datestring, "%m/%d/%Y %H:%M:%S").timestamp()
print(date)