import os
from bot.bot import SpeedDater

if __name__ == '__main__':
    bot = SpeedDater()
    bot.run(os.environ.get('TOKEN', '<--- Enter your bot token --->'))
