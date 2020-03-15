import os

from discord.ext import commands

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, prefix=None):
        if not prefix:
            p = await self.bot.get_prefix(ctx.message)
            await ctx.send(f'The guild prefix is `{p[-1]}`')
            return

        prevresult = self.bot.db['configs'].find( guild_id=ctx.guild.id )
        try:
            # Exhaust the generator, then get the first index
            prevdata = [d for d in prevresult][0]
            prevdata.__delitem__('id')
            data = prevdata
            data['prefix'] = prefix

        except IndexError:
            # Catch IndexError; The guild has not changed it's config yet
            default = dict(
                guild_id=ctx.guild.id,
                prefix=os.environ.get('prefix', '!'),
                duration=os.environ.get('duration', 300),
                delay=os.environ.get('delay', 30)
            )

            data = default
            data['prefix'] = prefix

        self.bot.db['configs'].upsert(data, ['guild_id'])
        await ctx.send(f'Guild prefix set to {prefix}')

    @commands.command()
    async def duration(self, ctx, duration=None):
        if not duration:
            results = [r for r in self.bot.db.find(guild_id=ctx.guild.id)]
            duration = results[-1]['duration'] if len(results) > 0 else os.environ.get('duration', 300)
            await ctx.send(f'The duration of the speed date is `{p[-1]}`')
            return
        prevresult = self.bot.db['configs'].find( guild_id=ctx.guild.id )
        try:
            # Exhaust the generator, then get the first index
            prevdata = [d for d in prevresult][0]
            prevdata.__delitem__('id')
            data = prevdata
            data['duration'] = duration

        except IndexError:
            # Catch IndexError; The guild has not changed it's config yet
            default = dict(
                guild_id=ctx.guild.id,
                prefix=os.environ.get('prefix', '!'),
                duration=os.environ.get('duration', 300),
                delay=os.environ.get('delay', 30)
            )

            data = default
            data['duration'] = duration

        self.bot.db['configs'].upsert(data, ['guild_id'])
        await ctx.send(f'Guild duration set to {duration}')

    @commands.command()
    async def delay(self, ctx, delay):
        prevresult = self.bot.db['configs'].find( guild_id=ctx.guild.id )
        try:
            # Exhaust the generator, then get the first index
            prevdata = [d for d in prevresult][0]
            prevdata.__delitem__('id')
            data = prevdata
            data['delay'] = delay

        except IndexError:
            # Catch IndexError; The guild has not changed it's config yet
            default = dict(
                guild_id=ctx.guild.id,
                prefix=os.environ.get('prefix', '!'),
                duration=os.environ.get('duration', 300),
                delay=os.environ.get('delay', 30)
            )

            data = default
            data['delay'] = delay

        self.bot.db['configs'].upsert(data, ['guild_id'])
        await ctx.send(f'Guild prefix set to {prefix}')


def setup(bot):
    bot.add_cog(Configuration(bot))
