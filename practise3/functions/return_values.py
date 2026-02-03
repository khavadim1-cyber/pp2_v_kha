def my_function():#function can return list
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])

def my_function(name, /):# positional-only argument, you cant use name="..." as argument
  print("Hello", name)

my_function("Emil")

def my_function(*, name):# keyword-only argument, you must use name="..." as argument
  print("Hello", name)

my_function(name="Emil")

def my_function(a, b, /, *, c, d):#you can mix positional and keyword arguments
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)