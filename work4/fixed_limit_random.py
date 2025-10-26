import random

class FixedLimit:
    def __init__(self, rate, limit, seed_num):

        self.success_rate = rate
        self.attempt = 0
        self.fixed_limit = limit
        random.seed(seed_num)

    def check_pity(self):

        num = random.uniform(0, 100)

        if num <= self.success_rate or self.attempt >= self.fixed_limit:
            self.attempt = 0
            return True
        else:
            self.attempt += 1
            return False

# test = FixedLimit(rate=30, limit=5, seed_num=2)

# for i in range(20):
#     test.check_pity()
    