import random

success_rate = 20
attempt = 1
fixed_limit = 5

for i in range(10):
    num = random.uniform(0, 100)

    if num <= success_rate or attempt >= fixed_limit:
        attempt = 0
        print("success!")
    else:
        print(f"fail.. | pity is {attempt} / 5")
        attempt += 1

    