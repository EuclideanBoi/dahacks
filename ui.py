import app
from app import Account
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Frame.winfo_toplevel(self).geometry("600x400")
        self._frame = None
        self.switch_frame(StartPage)
        self.user = None
    
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
        tk.Label(self, text="pretend theres transactions here").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Logout", command=lambda: self.logout()).pack()

    def logout(self, event = None):
        self.master.switch_frame(StartPage)

if __name__ == "__main__":
    app = App()
    app.mainloop()