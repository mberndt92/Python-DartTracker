from bots.bot_beginner import BeginnerBot
from bots.bot_9_darter import NineDartsBot
from dartboard import Dartboard
from pretty_printer import PrettyPrinter
from tkinter import *

bot = BeginnerBot()
target = bot.aim(score=501)
result = bot.throw(501)
print(result)

window = Tk()
window.config(pady=20, padx=20)



