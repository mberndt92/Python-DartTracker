from unittest import TestCase
from bots.bot_9_darter import NineDartsBot


class TestBotHelper(TestCase):

    def setUp(self):
        self.bot = NineDartsBot()
        self.average_score = 171
        self.delta = 0

    def test_average_score(self):
        score = 501
        for _ in range(10000):
            number, segment = self.bot.aim(score=score)
            self.bot.throw(number=number, segment=segment)

        avg_score = int(self.bot.average_three_dart_score())
        print(f"Average score for: {self.bot.name} is: ({avg_score})")
        self.assertAlmostEqual(self.average_score, avg_score, delta=self.delta)