import random

predetermin = random.randint(0, 10)
count = 0

for i in range(10):
    if count >= predetermin:
        count = 0
        predetermin = random.randint(0, 10)
        print(f"be attacked! next encounter is {predetermin}")
    else:
        count += 1
        print("...")
    