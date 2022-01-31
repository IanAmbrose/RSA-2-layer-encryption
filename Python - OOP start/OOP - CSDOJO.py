class Robot:
    def __init__(self,name,color,weight):
        self.name = name
        self.color = color
        self.weight = weight
    
    def introduceSelf(self):
        print(f'Hello my name is {self.name}')

class Person:
    def __init__(self, name, personality, isSitting):
        self.name = name
        self.personality = personality
        self.isSitting = isSitting

    def sit_down(self):
        self.isSitting = True

    def stand_up(self):
        self.isSitting = False




r1 = Robot('Ian', 'red', 50)
r2 = Robot('John', 'silver', 70)

r1.introduceSelf()

p1 = Person("Alice", "aggressive", False)
p2 = Person("Becky", "talkative", True)


p1.robot_owned = r2
p2.robot_owned = r1

print("This is a test")
#p1 owns r2

p1.robot_owned.introduceSelf()
