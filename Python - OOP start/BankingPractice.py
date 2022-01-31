#Parent Class: User
#Holds details about a user
#Has a function to show user details
#Child Class: Bank
#Stores details about the account balance
#Stroes details about the amount
#Allows for deposits, withdraw, view_balance


class User():
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def show_user_details(self):
        print("Personal Details")
        print(f'''User: {self.name}
                  Gender: {self.gender}
                  Age: {self.age}
             ''')


class Bank(User):

    def __init__(self, first, last, pin):
        pass
    def account_balance(self):
        pass

    def deposit(self):
        pass

    def withdraw(self):
        pass

    def view_balance(self):
        pass



p1 = User('Ian Ambrose', 'Male', 21)

p1.show_user_details()