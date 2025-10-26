import random

random.seed(1) # กำหนด seed เพื่อง่ายต่อการ debug
for i in range(10):
    print(random.randint(0,10), end=" ")