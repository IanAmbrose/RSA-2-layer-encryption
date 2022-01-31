#Python Object-Oriented programming

class Employee:  
    raise_amount = 1.05
    num_of_employees = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.num_of_employees += 1

    def fullname(self):
        return f'{self.first} {self.last}'

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amount = amount

class Developer(Employee):
    raise_amount = 1.03

    def __init__(self, first, last, pay, prog_language):
        super().__init__(first, last, pay)
        self.prog_lang = prog_language

class Manager(Employee):

    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
    
    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname())



emp_1 = Employee('Ian', 'Ambrose', 50000)
emp_2 = Employee('Ian', 'William', 50000)

dev_1 = Developer('Ian', 'AmbroseDEV', 20000, 'Python')
dev_2 = Developer('Ian', 'WilliamDEV', 20000, 'Java')

man_1 = Manager('Ian', 'AmbroseMAN', 100000, [dev_1])

#Employee.set_raise_amt(1.06)



