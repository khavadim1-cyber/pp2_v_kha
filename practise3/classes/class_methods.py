class Person:#Methods are functions that belong to a class. They define the behavior of objects created from the class.

  def __init__(sel, name):#You can use any name for self, but it must be the first in ()
    sel.name = name

  def greet(sel):
    print("Hello, my name is " + sel.name)

p1 = Person("Emil")
p1.greet()

class Calculator:
  def add(self, a, b):#methods of class
    return a + b

  def multiply(self, a, b):
    return a * b

calc = Calculator()#creating an object
print(calc.add(5, 3))
print(calc.multiply(4, 7))

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def get_info(self):
    return f"{self.name} is {self.age} years old"

p1 = Person("Tobias", 28)
print(p1.get_info())

class Person:#The __str__() method is a special method that controls what is returned when the object is printed:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def __str__(self):
    return f"{self.name} ({self.age})"

p1 = Person("Tobias", 36)
print(p1)