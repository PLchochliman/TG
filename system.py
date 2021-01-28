"""
here some utils for future - rebuilding for Discord server.
Preparations for rebuilding it in the future - now piece of sh*t
"""
from random import seed
from random import random

seed()

"""
rolls Dice. in Dice type you write maximum value of the dice. 
Returns int
TODO maybe do into generator????
"""


def rollDice(diceType):
    return int((random() * diceType)) + 1


"""
rolls multiple Dices. in Dice type you write maximum value of the dice. 
Returns tab of records
"""


def multiRollDice(diceType, countOfDices):
    result = []
    for i in range(0,countOfDices):
        result.append(rollDice(diceType))
    return result


"""
rolls multiple Dices. in Dice type you write maximum value of the dice. 
Returns sum of roll
"""


def sumMultiRollDice(diceType, countOfDices):
    result = 0
    for i in range(0,countOfDices):
        result = result + rollDice(diceType)
    return result


"""
basic Output command for the system. Awaits for being updated, when put into Discord BOT
"""
def Output(text):
    print(text)

def Input():
    return input()
