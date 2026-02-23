#ex1
import datetime
x = datetime.datetime.now()
y = datetime.timedelta(days = 5)
print(x-y)

#ex2
z=datetime.timedelta(days=1)
print(f"{x-z}, yesterday")
print(f"{x}, today")
print(f"{x+z}, tomorrow")

#ex3
print(x.strftime("%Y-%m-%d %H:%M:%S"))

#ex4
from datetime import datetime
a=datetime.strptime(input(),"%Y-%m-%d %H:%M:%S")
b=datetime.strptime(input(),"%Y-%m-%d %H:%M:%S")
print(abs(int((b-a).total_seconds())))
