
from dartboard import Dartboard
from random import choice, randint
from bots.dart_bot import DartBot
from bots.constants import TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE, TARGET_TYPE_TRIPLE


class NineDartsBot(DartBot):

    def __init__(self):
        super().__init__(
            name="9 Darter",
            singles=1,
            doubles=1,
            triples=1,
            bull=1,
            double_bull=1,
            miss_chance=1,
            miss_after_doubles=1
        )

    @staticmethod
    def __calculate_target(score):
        # Uber-Bot
        if score <= 40 and score % 2 == 0:
            return score / 2, TARGET_TYPE_DOUBLE
        elif score <= 40 and score % 2 != 0:
            return 1, TARGET_TYPE_SINGLE  # Should never happen, this is a 9-Darter bot
        elif score % 2 == 0:
            return 20, TARGET_TYPE_TRIPLE
        else:
            return 19, TARGET_TYPE_TRIPLE

    def __probability_table(self):
        table = {
            number: {
                TARGET_TYPE_SINGLE: self.singles_accuracy
                if TARGET_TYPE_SINGLE in Dartboard.get_valid_target_types(number) else None,

                TARGET_TYPE_DOUBLE: self.doubles_accuracy
                if TARGET_TYPE_DOUBLE in Dartboard.get_valid_target_types(number) else None,

                TARGET_TYPE_TRIPLE: self.triples_accuracy
                if TARGET_TYPE_TRIPLE in Dartboard.get_valid_target_types(number) else None
            }
            for number in Dartboard.all_numbers()
        }

        # Update Bulls probability
        table[25][TARGET_TYPE_SINGLE] = self.bull_accuracy
        table[25][TARGET_TYPE_DOUBLE] = self.double_bull_accuracy

        return table
