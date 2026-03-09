import os
os.makedirs("test/a/b", exist_ok=True)
print(os.listdir("."))