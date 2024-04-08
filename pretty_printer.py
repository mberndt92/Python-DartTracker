
from constants import TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE, TARGET_TYPE_TRIPLE


class PrettyPrinter:

    @staticmethod
    def target_to_pretty(number, target_type):
        prefix = ""
        magic_number = number
        if number == 25:
            magic_number = "Bull"
        if target_type == TARGET_TYPE_DOUBLE:
            prefix = "D"
        elif target_type == TARGET_TYPE_TRIPLE:
            prefix = "T"
        return f"{prefix}{magic_number}"

    @staticmethod
    def print_probability_table(table):
        for number, target_types in table.items():
            target_values = []
            for target_type, probability in target_types.items():
                target_values.append(
                    f"{PrettyPrinter.target_to_pretty(number=number, target_type=target_type)}: {probability}"
                )
            print(f"{'|'.join(target_values)}")
