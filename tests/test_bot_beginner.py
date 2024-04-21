from bots.bot_beginner import BeginnerBot
from test_bot_helper import TestBotHelper


class TestBeginnerBot(TestBotHelper):

    def setUp(self):
        self.bot = BeginnerBot()
        self.average_score = 60
        self.delta = 10
