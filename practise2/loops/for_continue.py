fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

for x in range(6):#else in for loop
  print(x)
else:
  print("Finally finished!")

adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:#nested loops
  for y in fruits:
    print(x, y)

for x in [0, 1, 2]:#pass
  pass