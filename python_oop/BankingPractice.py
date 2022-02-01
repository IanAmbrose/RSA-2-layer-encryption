#Parent Class: User
#Holds details about a user
#Has a function to show user details
#Child Class: Bank
#Stores details about the account balance
#Stroes details about the amount
#Allows for deposits, withdraw, view_balance

#Parent Class
class User():
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def show_user_details(self):
        print("Personal Details\n")
        print(f'User:{self.name}\nGender: {self.gender}\nAge: {self.age} ')

#Child Class
class Bank(User):

    def __init__(self, name, gender, age):
        super().__init__(name, gender, age)
        self.balance = 0

    def view_balance(self):
        self.show_user_details()
        print(f'Balance: £{self.balance}')

    def deposit(self, amount):
        self.amount = amount
        self.balance = self.balance + amount
        print(f'Account balance has been updated £{self.balance}')

    def withdraw(self, amount): 
        self.amount = amount
        if self.amount > self.balance:
            print(f'Insufficient Funds | Balance available £{self.balance}')
        else:
            self.balance = self.balance - amount
            print(f'Account balance has been updated £{self.balance}')

p1 = User('Ian Ambrose', 'Male', 21)
b1 = Bank('Ian AmbroseBank', 'Male', 21)


p1.show_user_details()
b1.deposit(500)
b1.withdraw(150)
b1.view_balance()
