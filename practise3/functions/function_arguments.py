def my_function(fname):#fname is a parameter
  print(fname + " Refsnes")

my_function("Emil")#"Emil" is an argument
my_function("Tobias")
my_function("Linus")

def my_function(fname, lname):#its possible to have more than one parameter
  print(fname + " " + lname)

my_function("Emil", "Refsnes")#but number of parameters must be equal to number of arguments

def my_function(name = "friend"):#You can assign default values to parameters. If the function is called without an argument, it uses the default value:
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

def my_function(person):#You can also send dictionaries or lists as arguments
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)