import random

class ProgressProb:
    def __init__(self, rate,seed_num):
        self.start_success_rate = rate
        self.success_rate = self.start_success_rate
        random.seed(seed_num)

    def rate(self):
        num = random.uniform(0, 100)

        if num <= self.success_rate:
            self.success_rate = self.start_success_rate
            print("success!")
        else:
            self.success_rate += 5
            print(f"fail.. | your success rate is {self.success_rate}")
    