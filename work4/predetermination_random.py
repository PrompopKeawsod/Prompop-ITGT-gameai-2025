import random

class Predetermin:
    
    def __init__(self, max_attempt, seed_num):
        
        self.max_attempt = max_attempt
        self.predetermin = random.randint(0, self.max_attempt)
        self.count = 0
        random.seed(seed_num)

    def check_predetermin(self):

        if self.count >= self.predetermin:
            self.count = 0
            self.predetermin = random.randint(0, self.max_attempt)
            return True
        else:
            self.count += 1

            return False
        
# test = Predetermin(max_attempt=10, seed_num=1)

# for i in range(20):
#     test.check_predetermin()
    