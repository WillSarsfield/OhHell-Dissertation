import random

def chooseCard(options):
    rnd = random.randrange(0, len(options))
    return options[rnd]

def chooseBid(ban):
    rnd = ban
    while rnd == ban:
        rnd = random.randrange(0, 13)
    return rnd
