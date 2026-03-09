from functools import reduce

nums = [1,2,3,4,5]
squares = list(map(lambda x: x*x, nums))
even = list(filter(lambda x: x%2==0, nums))
total = reduce(lambda a,b: a+b, nums)

print(squares)
print(even)
print(total)