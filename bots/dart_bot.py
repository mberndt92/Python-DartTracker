from dartboard import Dartboard
from random import choice, randint, uniform
from .constants import TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE, TARGET_TYPE_TRIPLE, TARGET_TYPE_MISS
from pretty_printer import PrettyPrinter

IS_DEBUG_MODE = False


# The Default Bot is a 9-Darter Bot
class DartBot:

    def __init__(
            self,
            name="DartBot",
            singles=1.0,
            doubles=1.0,
            triples=1.0,
            bull=1.0,
            double_bull=1.0,
            miss_chance=0.0,
            miss_after_doubles=0.0
    ):
        self.name = name
        self.singles_accuracy = singles
        self.doubles_accuracy = doubles
        self.triples_accuracy = triples
        self.bull_accuracy = bull
        self.double_bull_accuracy = double_bull
        self.miss_chance = miss_chance
        self.miss_after_doubles = miss_after_doubles
        self.blackies = 0
        self.throws = 0
        self.score = 0

    def average_three_dart_score(self):
        return (self.score / self.throws) * 3

    @staticmethod
    def aim(score):
        return DartBot.__calculate_target(score=score)

    def throw(self, number, segment):
        probability = self.__calculate_probability(number=number, segment=segment)

        is_miss = self.__is_missed_shot()
        if is_miss:
            self.blackies += 1
            return number, TARGET_TYPE_MISS

        roll = randint(0, 100)
        is_hit = roll <= probability * 100

        if IS_DEBUG_MODE:
            DartBot.__debug_print_shot_details(
                number=number,
                segment=segment,
                probability=probability,
                roll=roll,
                is_hit=is_hit
            )

        if is_hit:
            return self.__hit_target(number=number, segment=segment)
        else:
            number, target_type = self.__calculate_actual_segment_hit(
                number=number,
                target_type=segment,
                roll=roll,
                probability=probability
            )
            self.__missed_target(number=number, segment=target_type, probability=probability, roll=roll)
            return number, target_type

    def __is_missed_shot(self):
        return randint(0, 100) < self.miss_chance

    def __hit_target(self, number, segment):
        self.throws += 1
        self.score += Dartboard.calculate_score(number=number, target_type=segment)
        return number, segment

    def __missed_target(self, number, segment, probability, roll):
        if IS_DEBUG_MODE:
            print(f"After missing the actual target, the new target is: {number} | segment: {segment}")
        self.throws += 1
        self.score += Dartboard.calculate_score(number=number, target_type=segment)

    @staticmethod
    def __debug_print_shot_details(number, segment, probability, roll, is_hit):
        pretty_printer = PrettyPrinter()
        target_text = f"Target: {pretty_printer.target_to_pretty(number=number, target_type=segment)}"
        probability_text = f" ({probability * 100}%)"
        is_hit_text = f" -> Hit! ({roll})" if is_hit else f" -> Miss ({roll})"
        print(target_text + probability_text + is_hit_text)

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

    def __calculate_probability(self, number, segment):
        table = self.__probability_table()
        return table[number][segment]

    def __attempted_reroll(self, target_type, roll, probability):
        is_hit = False
        hit_type = TARGET_TYPE_MISS
        # If target was TRIPLE, re-roll for a single
        if target_type == TARGET_TYPE_TRIPLE:
            single_roll = randint(0, 100)
            is_hit = single_roll <= self.singles_accuracy
            hit_type = TARGET_TYPE_SINGLE
        # If target was DOUBLE, re-roll for a MISS/SINGLE
        elif target_type == TARGET_TYPE_DOUBLE:
            out_of_bounds_or_single_roll = randint(0, 100)
            is_hit = out_of_bounds_or_single_roll <= self.miss_after_doubles
            if is_hit:
                hit_type = TARGET_TYPE_MISS
            else:
                is_hit = out_of_bounds_or_single_roll <= self.singles_accuracy
                if is_hit:
                    hit_type = TARGET_TYPE_SINGLE
        # If target was SINGLE, re-roll for TRIPLE/DOUBLE
        elif target_type == TARGET_TYPE_SINGLE:
            t_and_d_roll = randint(0, 100)
            is_hit = t_and_d_roll <= self.triples_accuracy
            if is_hit:
                hit_type = TARGET_TYPE_TRIPLE
            else:
                is_hit = t_and_d_roll <= self.doubles_accuracy
                hit_type = TARGET_TYPE_DOUBLE

        return is_hit, hit_type

    def __calculate_actual_segment_hit(self, number, target_type, roll, probability):
        is_hit, hit_type = self.__attempted_reroll(target_type=target_type, roll=roll, probability=probability)

        if IS_DEBUG_MODE:
            print(f"After re_rolling, the new result is hit: {is_hit} | segment: {hit_type}")

        if is_hit:
            return number, hit_type

        all_numbers = Dartboard.all_numbers()

        # random pick from the list
        actual_number_hit = choice(all_numbers)

        # pick target_type
        if actual_number_hit == 25:
            relevant_values = [self.bull_accuracy, self.double_bull_accuracy]
        else:
            relevant_values = [self.singles_accuracy, self.doubles_accuracy, self.triples_accuracy]

        # TODO: also roll on the segment!
        # Very pragmatic mapping here. Needs refactoring when utilising the actual probability table beyond initial hit
        values = [self.singles_accuracy, self.doubles_accuracy, self.triples_accuracy]
        mapped_segments = [TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE, TARGET_TYPE_TRIPLE]

        upper_limit = sum(values)
        segment_roll = uniform(0, upper_limit)

        # TODO: Not sure this code works as expected
        right_border = values[0]
        actual_segment_hit = TARGET_TYPE_SINGLE
        for i in range(len(values)):
            if segment_roll <= right_border:
                actual_segment_hit = mapped_segments[i]
                break
            right_border += values[i]

        if target_type == actual_segment_hit:
            actual_segment_hit = TARGET_TYPE_SINGLE

        pretty_printer = PrettyPrinter()

        if IS_DEBUG_MODE:
            print(f"{pretty_printer.target_to_pretty(number=actual_number_hit, target_type=actual_segment_hit)}")
        return actual_number_hit, actual_segment_hit
