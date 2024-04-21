from bots.bot_beginner import BeginnerBot
from bots.bot_9_darter import NineDartsBot
from dartboard import Dartboard
from pretty_printer import PrettyPrinter


def simulate_game():
    dartboard = Dartboard()
    nine_darter_bot = NineDartsBot()
    beginner_bot = BeginnerBot()

    score1 = 501
    score2 = 501
    pretty_printer = PrettyPrinter()
    print(f"Scores: {score1} | {score2}")
    while score1 > 0 and score2 > 0:
        number, segment = beginner_bot.aim(score=score1)
        number, segment = beginner_bot.throw(number=number, segment=segment)
        score1 -= dartboard.calculate_score(number=number, target_type=segment)
        score1 = max(score1, 0)

        number, segment = nine_darter_bot.aim(score=score2)
        number, segment = nine_darter_bot.throw(number=number, segment=segment)
        score2 -= dartboard.calculate_score(number=number, target_type=segment)
        score2 = max(score2, 0)

        print(f"Scores: {score1} | {score2}")


def simulate_neighbours_check():
    test_numbers = [20, 19, 18, 17, 16, 15, 25]
    for number in test_numbers:
        neighbours = Dartboard.get_neighbours(number, 10)
        print(f"Neighbours for: {number}: {neighbours}")
