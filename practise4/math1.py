import math
n=int(input("Input degree:"))#ex1
a=math.pi
y=n*a/180
print(f"Output radian: {y:.6f}")

#ex2
a=int(input("Height: "))
b=int(input("Base, first value: "))
c=int(input("Base, second value: "))
print((c+b)/2 * a)

#ex3
b=int(input("Input number of sides: "))
c=int(input("Input the length of a side: "))
x=int((b * pow(c,2))/ (4 * math.tan(math.pi/b)))
print(f"The area of the polygon is: {x}")

#ex4
a=int(input("Length of base: "))
b=int(input("Height of parallelogram: "))
print(f"Area of parallelogram: {a*b:.1f}")