import os

import dataset
import discord
from discord.ext import commands

class SpeedDater(commands.Bot):
    def __init__(self, db=None):
        super().__init__(self, command_prefix=self.get_prefix)

        self.db = db or dataset.connect('sqlite:///speeddate.db')


    def get_prefix(self, bot, message):
        if not isinstance(message.channel, discord.abc.GuildChannel):
            return commands.when_mentioned_or(os.environ.get('prefix', '!'))

        result = self.db['configs'].find(guild_id=message.guild.id)
        prefix = result.next()['prefix'] if len( [r for r in result] ) > 0 else os.environ.get('prefix', '!')

        return commands.when_mentioned_or(prefix)


    async def on_ready(self):
        print(  f"Connected to {len(self.bot.users)} users",
                f"from {len(self.bot.guilds)} guilds\n\n------------")

        print('Loading cogs')
        for file in os.listdir( os.path.join(os.getcwd(),'bot','cogs') ):
            if file.endswith('.py'):
                print(f'Loading: bot.cogs.{file}')
                self.load_extension(f'bot.cogs.{file}')
