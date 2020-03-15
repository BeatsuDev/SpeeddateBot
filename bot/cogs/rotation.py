import asyncio
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
        self.waiting_line = []

    @commands.is_owner()
    @commands.command()
    async def signup(self, ctx):
        self.users = []
        embed=discord.Embed(
            title="Bli med i Kattas speed date!",
            description=(
                "De siste dagene kan ha virket helt surrealistisk og nå har vi mye tid å tilbringe hjemme. "
                "Her har du muligheten til å snakke med andre medelever og bli kjent med nye folk eller "
                "fortelle det du har på hjertet! Under er det noen forslag om hva man kan snakke om.\n"
            ),
            color=0x00ff00
        )

        embed.set_thumbnail(url="https://www.northwestern.edu/counseling/outreach-education/lets-talk/assets/Lets-talk1.jpg")
        embed.add_field(
            name="**Deg selv!**",
            value="Hva har du gått igjennom?",
            inline=True
        )
        embed.add_field(
            name="**Ting du er glad for/i**",
            value="Hva liker du at du har i livet ditt?",
            inline=True
        )
        embed.add_field(
            name="**Hobby & Fritid**",
            value="Hva driver du med hjemme 'a?",
            inline=True
        )
        embed.add_field(
            name="**Hva synes du om skolen?**",
            value="Trives du? Hva mener du kunne vært bedre?",
            inline=True
        )
        embed.set_footer(
            text="Trykk på checkmarken under for å bli med!",
            icon_url="https://i.pinimg.com/originals/a6/5c/4a/a65c4ae1e6a70af74a70ec2fe946e2e8.png"
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✅')

        check = lambda r, u: r.message.id == msg.id and not (u.id in self.users)
        while len(self.users) < 16 and not self.running:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=300)
                if not self.running:
                    self.users.append(user.id)
            except asyncio.TimeoutError:
                await ctx.send(f'Timed out at signup reaction add | Start with {len(self.users)} members or re-sign up!')
                return


    @commands.is_owner()
    @commands.command()
    async def start(self, ctx):
        self.running = True
        await ctx.message.add_reaction('👌')

        self.users = self.users if self.users%2==0 else self.waiting_line.append(self.users.pop())


        for _ in range(2):
            # How many times to rotate; meaning 2 rotations = 3 conversations
            # Get talk duration from DB
            result = bot.db['configs'].find(guild_id=message.guild.id)
            results = [r for r in result]
            duration = results[0]['duration'] if len( results ) > 0 else os.environ.get('duration', 300)
            await asyncio.sleep(duration)

            # Rotate users
            

        self.users = []
        self.waiting_line = []

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after == None and self.running:
            self.users.remove(member.id)
            if len(self.waiting_line) > 0:
                newmember = member.guild.get_user(self.waiting_line[0])
                await newmember.move_to(before)


def setup(bot):
    bot.add_cog(Rotation(bot))
