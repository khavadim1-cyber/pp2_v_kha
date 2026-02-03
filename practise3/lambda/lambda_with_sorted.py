students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]#The sorted() function can use a lambda as a key for custom sorting:
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)