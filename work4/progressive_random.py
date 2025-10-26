import random

class ProgressProb:
    def __init__(self, rate,seed_num):
        self.start_success_rate = rate
        self.success_rate = self.start_success_rate
        random.seed(seed_num)

    def chance(self):
        num = random.uniform(0, 100)

        if num <= self.success_rate:
            self.success_rate = self.start_success_rate
            return True
        else:
            self.success_rate += 5
            return False
        
# randomprob = ProgressProb(rate=20, seed_num=2)

# for i in range(10):
#     randomprob.rate()
    