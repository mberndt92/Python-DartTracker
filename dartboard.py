
from constants import TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE, TARGET_TYPE_TRIPLE, TARGET_TYPE_MISS


class Dartboard:

    @staticmethod
    def all_numbers():
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]

    @staticmethod
    def get_valid_target_types(number):
        if number == 25:
            return [TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE]
        else:
            return [TARGET_TYPE_SINGLE, TARGET_TYPE_DOUBLE, TARGET_TYPE_TRIPLE]

    @staticmethod
    def calculate_score(number, target_type):
        if target_type == TARGET_TYPE_SINGLE:
            return number
        elif target_type == TARGET_TYPE_DOUBLE:
            return number * 2
        elif target_type == TARGET_TYPE_TRIPLE:
            return number * 3
        elif target_type == TARGET_TYPE_MISS:
            return 0
        else:
            print(f"Invalid hit type: number: {number} | type: {target_type}")
            return 0

    @staticmethod
    def __neighbouring_table():
        return {
            20: [5, 1],
            1: [20, 18],
            18: [1, 4],
            4: [18, 13],
            13: [4, 6],
            6: [13, 10],
            10: [6, 15],
            15: [10, 2],
            2: [15, 17],
            17: [2, 3],
            3: [17, 19],
            19: [3, 7],
            7: [19, 16],
            16: [7, 8],
            8: [16, 11],
            11: [8, 14],
            14: [11, 9],
            9: [14, 12],
            12: [9, 5],
            5: [12, 20],
            25: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        }

    @staticmethod
    def get_neighbours(number, max_distance):
        table = Dartboard.__neighbouring_table()
        neighbours = table[number]
        max_distance -= 1

        checked_numbers = [number]
        while max_distance > 0 and len(set(checked_numbers)) < 21:
            new_neighbours = []
            for neighbour in neighbours:
                if neighbour not in checked_numbers:
                    new_neighbours.extend(table[neighbour])
                    checked_numbers.append(neighbour)
            neighbours.extend(new_neighbours)
            max_distance -= 1

        neighbours = list(set(neighbours))
        if number in neighbours:
            neighbours.remove(number)

        return neighbours
