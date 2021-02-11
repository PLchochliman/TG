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


def roll_dice(diceType):
    return int((random() * diceType)) + 1


"""
rolls multiple Dices. in Dice type you write maximum value of the dice. 
Returns tab of records
"""


def multi_roll_dice(diceType, countOfDices):
    result = []
    for i in range(0, countOfDices):
        result.append(roll_dice(diceType))
    return result


"""
rolls multiple Dices. in Dice type you write maximum value of the dice. 
Returns sum of roll
"""


def sum_multi_roll_dice(diceType, countOfDices):
    result = 0
    for i in range(0, countOfDices):
        result = result + roll_dice(diceType)
    return result

"""
"""

def roll_dice_from_text(text):
    result = 0
    text = text.lower()
    if text.startswith("d"):
        return roll_dice(int(text[1:]))
    else:
        text = text.split("d")
        return sum_multi_roll_dice(int(text[0]), int(text[1]))

"""
basic Output command for the Bot. Awaits for being updated, when put into Discord BOT
"""
def output(text):
    print(text)


def input_for_bot():
    nowy = input()
    return nowy.lower()
