class MyClass:#class defenition
  x = 5
  y =6
p=MyClass()#p-object
print(p.y, p.x)

p1 = MyClass()#creating multiple objects
p2 = MyClass()
p3 = MyClass()
print(p1.x)
print(p2.x)
print(p3.x)

class Person:#class cant be empty
  pass

del p1#deleting object
