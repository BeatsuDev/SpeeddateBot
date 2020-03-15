import discord
from discord.ext import commands
from stuf import stuf

# roleid: (Text, Voice)
rooms = stuf({
    'rom1': {
        'role_id': 688543432716845128,
        'text_channel': 688542752140820536,
        'voice_channel': 688542950166233121
    },
    'rom2': {
        'role_id': 688543435539349602,
        'text_channel': 688542768091365397,
        'voice_channel': 688543249836539906

    },
    'rom3': {
        'role_id': 688543439918465257,
        'text_channel': 688542792213200912,
        'voice_channel': 688543285182070805

    },
    'rom4': {
        'role_id': 688543440656793642,
        'text_channel': 688542809694666836,
        'voice_channel': 688543309945110530

    },
    'rom5': {
        'role_id': 688543442699288597,
        'text_channel': 688542824152563804,
        'voice_channel': 688543332695015458

    },
    'rom6': {
        'role_id': 688543443307462905,
        'text_channel': 688542838795141150,
        'voice_channel': 688545447400571032

    },
    'rom7': {
        'role_id': 688543444771143798,
        'text_channel': 688542897489969184,
        'voice_channel': 688543360276758555

    },
    'rom8': {
        'role_id': 688543445773844483,
        'text_channel': 688542911197085760,
        'voice_channel': 688543387959164960

    }
})

class Rotation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.users = []

    @commands.command()
    async def signup(self, ctx):
        embed = discord.Embed()

        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✅')

        check = lambda m: m.id == msg.id and not (m.author.id in self.users)

        while len(self.users) < 16 and not self.running:
            reaction, user = self.bot.wait_for('reaction_add', check=check, timeout=300)



def setup(bot):
    bot.add_cog(Rotation(bot))
