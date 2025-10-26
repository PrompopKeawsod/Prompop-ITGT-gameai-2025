import random
class MarbleBag:
    def __init__(self, items, probs, seed_num):
        self.bag = []
        self.items = items
        self.probs = probs
        self.fill_bag()
        random.seed(seed_num)

    def fill_bag(self):
        for i in range(len(self.items)):
            self.bag += [self.items[i]] * self.probs[i]

    def random_item(self):
        item = random.choice(self.bag)
        self.bag.remove(item)
        if len(self.bag) <= 0:
            self.fill_bag()
        return item

# items = ["dirt", "monster", "gold"]
# probs = [7, 2, 1]
# marblebag = MarbleBag(items=items, probs=probs, seed_num=2)

# for i in range(20):
#     draw_item = marblebag.random_item()
#     print(draw_item, end=" ")