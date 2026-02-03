def my_function(): #def word creates a function
  print("i want to escape from university")

my_function()

def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

def get_greeting():#function can return a value
  return "Hello from a function"

message = get_greeting()
print(message)#we can see the result of a function with 2 ways
print(get_greeting())

def my_function():#if there is no code yet in the function
  pass