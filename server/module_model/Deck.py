import random


class Deck:

    def __init__(self):
        self.cards = list(range(2, 99))
        self.mix_cards()

    def mix_cards(self):
        random.shuffle(self.cards)

    def handout_card(self):
        return self.cards.pop(0)
