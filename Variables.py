x = 5 # example 1
y = "John"
print(x)
print(y)

a = "Python" # example 2
b= "is"
c = "awesome"
print(a, b, c)

fruits = ["apple", "banana", "cherry"]
z, m, h = fruits
print(z)
print(m)
print(h)

q = "awesome" # example 4
def myfunc():
  print("Python is " + q)
myfunc()

w = "awesome" # example 5
def myfunction():
  global w
  w = "fantastic"

myfunction()
print("Python is " + w)

