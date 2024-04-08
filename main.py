from bots.bot_beginner import BeginnerBot
from bots.bot_9_darter import NineDartsBot
from bots.dart_bot import DartBot
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
        number, segment = beginner_bot.throw(score=score1)
        score1 -= dartboard.calculate_score(number=number, target_type=segment)
        score1 = max(score1, 0)
        pretty_number = pretty_printer.target_to_pretty(number=number, target_type=segment)

        number, segment = nine_darter_bot.throw(score=score2)
        score2 -= dartboard.calculate_score(number=number, target_type=segment)
        score2 = max(score2, 0)
        pretty_number_2 = pretty_printer.target_to_pretty(number=number, target_type=segment)

        print(f"Scores: {score1} | {score2}")

    # beginner_bot.print_statistics()
    # nine_darter_bot.print_statistics()


def simulate_neighbours_check():
    test_numbers = [20, 19, 18, 17, 16, 15, 25]
    for number in test_numbers:
        neighbours = Dartboard.get_neighbours(number, 10)
        print(f"Neighbours for: {number}: {neighbours}")


# bot = BeginnerBot()
# target = bot.aim(score=501)
# result = bot.throw(501)
# print(result)
