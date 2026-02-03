def my_function(*kids):#if we dont know how many arguments will be passed we use *args 
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")

def my_function(*numbers):#*args is useful when you want to create flexible functions:


  total = 0
  for num in numbers:
    total += num
  return total

print(my_function(1, 2, 3))
print(my_function(10, 20, 30, 40))
print(my_function(5))

def my_function(**myvar):# **kwargs is the same ass *args, but instead of a tuple of arguments, it's a dictionary:
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function(name = "Tobias", age = 30, city = "Bergen")

def my_function(title, *args, **kwargs):# its possible to use both *args and **kwargs
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

my_function("User Info", "Emil", "Tobias", age = 25, city = "Oslo")

def my_function(a, b, c):#If you have values stored in a list, you can use * to unpack them into individual arguments:
  return a + b + c

numbers = [1, 2, 3]
result = my_function(*numbers) # Same as: my_function(1, 2, 3)
print(result)