
from dartboard import Dartboard
from random import choice, randint
# from "./bots/" constants import TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE, TARGET_TYPE_TRIPLE
from bots.dart_bot import DartBot
from bots.constants import TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE, TARGET_TYPE_TRIPLE


class BeginnerBot(DartBot):

    def __init__(self):
        super().__init__(
            name="Beginner",
            singles=0.35,
            doubles=0.15,
            triples=0.10,
            bull=0.20,
            double_bull=0.10,
            miss_chance=0.10,
            miss_after_doubles=0.4
        )

    @staticmethod
    def __calculate_target(score):
        target_type = TARGET_TYPE_TRIPLE if randint(0, 100) > 35 else TARGET_TYPE_SINGLE
        target_number = 20
        if score > 170:
            target_number = choice([20, 19, 18, 17, 16, 15, 25])
        elif score == 50:
            target_number = score / 2
            target_type = TARGET_TYPE_DOUBLE
        elif score <= 40:
            if score % 2 == 0:
                target_number = score / 2
                target_type = TARGET_TYPE_DOUBLE
        else:
            dartboard = Dartboard()
            target_number = choice(dartboard.all_numbers())

        if target_number == 25 and target_type == TARGET_TYPE_TRIPLE:
            target_type = TARGET_TYPE_DOUBLE

        return target_number, target_type

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
