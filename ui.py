import app
from app import Account
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Frame.winfo_toplevel(self).geometry("600x400")
        self._frame = None
        self.switch_frame(StartPage)
        self.user = None
        self.account = None
    
    def switch_frame(self, frame):
        new_frame = frame(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Login", command=lambda: master.switch_frame(Login)).pack()
        tk.Button(self, text="Register", command=lambda: master.switch_frame(Register)).pack()

class Login(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Login page").pack(side="top", fill="x", pady=10)

        self.accountField = ttk.Entry(self, text="Account Name")
        self.usernameField = ttk.Entry(self, text="Username")
        self.passwordField = ttk.Entry(self, text="Password", show='*')

        self.accountField.focus_set()
        self.passwordField.bind('<Return>', self.authenticate)

        self.accountField.pack(pady=10)
        self.usernameField.pack(pady=10)
        self.passwordField.pack(pady=10)

        tk.Button(self, text="Log In", command=lambda: self.authenticate()).pack()

        tk.Button(self, text="Return", command=lambda: master.switch_frame(StartPage)).pack()

    def authenticate(self, event = None):
        accountName = self.accountField.get()
        username = self.usernameField.get()
        password = self.passwordField.get()

        self.master.account = Account(accountName)
        self.master.account.getExisting()

        if self.master.account.useUser(username, password):
            self.master.switch_frame(Main)
        else:
            self.master.switch_frame(Login)

class Register(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Registration page: Enter account name and root password, sign in with root").pack(side="top", fill="x", pady=10)
        self.accountField = ttk.Entry(self, text="Account Name")
        self.passwordField = ttk.Entry(self, text="Root Password", show='*')

        self.accountField.focus_set()
        self.passwordField.bind('<Return>', self.register)

        self.accountField.pack(pady=10)
        self.passwordField.pack(pady=10)

        tk.Button(self, text="Register", command=lambda: self.register()).pack()

        tk.Button(self, text="Return", command=lambda: master.switch_frame(StartPage)).pack()

    def register(self, event = None):
        accountName = self.accountField.get()
        password = self.passwordField.get()

        self.master.account = Account(accountName)

        if self.master.account.registerAccount(password):
            self.master.switch_frame(Login)

class Main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Transactions").pack(side="top", fill="x", pady=10)

        self.transactionList = tk.Listbox(self, width=300)
        balanceSheet = self.master.account.getTransactions()
        balance = 0.00
        for x in balanceSheet:
            balance += float(x[3])
            self.transactionList.insert(tk.END, x)
        balance = str(round(balance, 2))

        tk.Label(self, text="Balance: " + balance).pack(side="top", fill="x", pady=10)

        self.transactionList.pack(side="top", fill="x", pady=10, padx=10)

        tk.Button(self, text="New Transaction", command=lambda: master.switch_frame(Transaction)).pack()
        tk.Button(self, text="Run Regression Analysis", command=lambda: master.switch_frame(Analysis)).pack()

        if self.master.account.currentUser == "root":
            tk.Button(self, text="(root) Create new user", command=lambda: master.switch_frame(NewUser)).pack()

        tk.Button(self, text="Logout", command=lambda: self.logout()).pack()

    def logout(self, event = None):
        self.master.account = None
        self.master.user = None
        self.master.switch_frame(StartPage)

class Transaction(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="New Transaction").pack(side="top", fill="x", pady=10)
        tk.Label(self, text="Enter amount and description:").pack(side="top", fill="x", pady=10)

        self.amountField = ttk.Entry(self, text="Amount")
        self.descriptionField = ttk.Entry(self, text="Description")

        self.amountField.pack(pady=10)
        self.descriptionField.pack(pady=10)

        tk.Button(self, text="Commit to Ledger", command=lambda: self.postTransaction()).pack()
        tk.Button(self, text="Cancel", command=lambda: master.switch_frame(Main)).pack()

    def postTransaction(self, event = None):
        amount = self.amountField.get()
        description = self.descriptionField.get()

        self.master.account.newTransaction(float(amount), description)

        self.master.switch_frame(Main)

class Analysis(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Data Analysis").pack(side="top", fill="x", pady=10)
        tk.Label(self, text="Enter prediction timestamp:").pack(side="top", fill="x", pady=10)

        self.timeField = ttk.Entry(self, text="Time")

        self.timeField.pack(pady=10)

        tk.Button(self, text="Run Regression", command=lambda: self.regress()).pack()
        tk.Button(self, text="Return", command=lambda: master.switch_frame(Main)).pack()

    def regress(self, event = None):
        time = int(self.timeField.get())

        pred = self.master.account.regression(time)

        tk.Label(self, text="Predicted change: $" + str(pred[2])).pack(side="top", fill="x", pady=10)

        '''
        x = pred[0]
        y = pred[1]
        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=1.0)
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        '''

class NewUser(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="New User").pack(side="top", fill="x", pady=10)
        tk.Label(self, text="Enter username, password, and root password:").pack(side="top", fill="x", pady=10)

        self.newUsernameField = ttk.Entry(self, text="Username")
        self.newPasswordField = ttk.Entry(self, text="Password", show='*')
        self.rootField = ttk.Entry(self, text="Root Password", show='*')

        self.newUsernameField.pack(pady=10)
        self.newPasswordField.pack(pady=10)
        self.rootField.pack(pady=10)

        tk.Button(self, text="Register", command=lambda: self.postUser()).pack()
        tk.Button(self, text="Cancel", command=lambda: master.switch_frame(Main)).pack()

    def postUser(self, event = None):
        username = self.newUsernameField.get()
        password = self.newPasswordField.get()
        rootPass = self.rootField.get()

        self.master.account.registerUser(username, password, rootPass)

        self.master.switch_frame(Main)

if __name__ == "__main__":
    app = App()
    app.mainloop()