class Person:#parent class
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

p1 = Student("Mike", "Olsen", 2019)
p1.welcome()

class T(Student):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname, year)

p2=T("Emil", "Refsnes", 2019)
p2.welcome()