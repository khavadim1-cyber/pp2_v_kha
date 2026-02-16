'''def square(n):
    for i in range(1, n+1):
        yield i * i
n = int(input())

for i in square(n):
    print(i)

n = int(input())
print(*(i for i in range(0, n + 1, 2)), sep=",")

def devisible(n):
    for i in range(n + 1):
        if i % 3 == 0 and i%4 ==0:
            yield i
n=int(input())
for i in devisible(n):
    print(i)'''

def squares(a,b):
    for i in range(a, b+1):
        yield i * i
a = int(input())
b= int(input())

for i in squares(a,b):
    print(i)

n=int(input())
print(*(i for i in range(n, -1, -1)), sep=" ")