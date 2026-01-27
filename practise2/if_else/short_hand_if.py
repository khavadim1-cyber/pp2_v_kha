a = 5#example1
b = 2
if a > b: print("a is greater than b")

a = 2#example2
b = 330
print("A") if a > b else print("B")

a = 10#example3
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

a = 330#example4
b = 330
print("A") if a > b else print("=") if a == b else print("B")

username = "" #example5
display_name = username if username else "Guest"
print("Welcome,", display_name)