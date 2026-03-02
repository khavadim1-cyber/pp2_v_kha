import re #ex from regex.md
n = input()
print("Match" if re.fullmatch("ab*",n)else "No match") #ex1
print("Match" if re.fullmatch("ab{2,3}",n)else "No match") #ex2
print(re.findall("[a-z]_[a-z]+",n)) #ex3
print( re.findall("[A-Z][a-z]+",n)) #ex4
print("Match" if re.fullmatch("a.*b",n)else "No match") #ex5
print(re.sub("[,. -]",":",n)) #ex6
print(re.sub("_([a-z])", lambda m: m.group(1).upper(), n)) #ex7
print(*re.split("[A-Z]",n))#ex8
print(re.sub("[A-Z]", " [A-Z]", n))#ex9
print(re.sub("([A-Z])", "_\1", n).lower().lstrip('_'))#ex10

