from bots.bot_9_darter import NineDartsBot
from test_bot_helper import TestBotHelper


class TestNineDartsBot(TestBotHelper):

    def setUp(self):
        self.bot = NineDartsBot()
        self.average_score = 171
        self.delta = 0
