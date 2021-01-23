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
"""
def rollDice(diceType):
    return int((random()* diceType)) + 1


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
basic Output command for the system. Awaits for being updated, when put into Discord BOT
"""
def Output(text):
    print(text)


"""
Test made of assertions, to not to loose the faith, in working code of this section
"""
def test():
    assert rollDice(4) > 0
    assert rollDice(4) < 5
    assert len(multiRollDice(4, 5)) < 6
    assert len(multiRollDice(4, 5)) > 4
    Output("System działa bez zarzutów")


#test()

"""
I know that I should do another file for unit test, and there is place for that. Maybe in future I'll do that.
"""
