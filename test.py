from Deck import Deck

deck = Deck()

deck.shuffle()

print("Deck:")

for card in deck.getCards():
    print(card)

print("Hand:")

for i in range(0,7):
    print(deck.pop())

print("Deck")

for card in deck.getCards():
    print(card)