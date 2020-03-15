import asyncio, os
import discord
from discord.ext import commands

# roleid: (Text, Voice)
defaultvoice = 688544744309260295
rooms = [
    {
        'role_id': 688543432716845128,
        'text_channel': 688542752140820536,
        'voice_channel': 688542950166233121
    },
    {
        'role_id': 688543435539349602,
        'text_channel': 688542768091365397,
        'voice_channel': 688543249836539906

    },
    {
        'role_id': 688543439918465257,
        'text_channel': 688542792213200912,
        'voice_channel': 688543285182070805

    },
    {
        'role_id': 688543440656793642,
        'text_channel': 688542809694666836,
        'voice_channel': 688543309945110530

    },
    {
        'role_id': 688543442699288597,
        'text_channel': 688542824152563804,
        'voice_channel': 688543332695015458

    },
    {
        'role_id': 688543443307462905,
        'text_channel': 688542838795141150,
        'voice_channel': 688545447400571032

    },
    {
        'role_id': 688543444771143798,
        'text_channel': 688542897489969184,
        'voice_channel': 688543360276758555

    },
    {
        'role_id': 688543445773844483,
        'text_channel': 688542911197085760,
        'voice_channel': 688543387959164960

    }
]

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

        check = lambda r, u: r.message.id == msg.id and not (u.id in self.users) and not u.bot
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

        if not len(self.users)%2==0:
            self.waiting_line.append(self.users.pop())

        textchannels = []
        voicechannels = []
        self.roles = []

        for i in range(len(self.users)):
            member = discord.utils.get(ctx.guild.members, id=self.users[i])

            text = discord.utils.get(ctx.guild.channels, id=rooms[i//2]['text_channel'])
            room = discord.utils.get(ctx.guild.voice_channels, id=rooms[i//2]['voice_channel'])
            role = discord.utils.get(ctx.guild.roles, id=rooms[i//2]['role_id'])

            textchannels.append(text)
            voicechannels.append(room)
            self.roles.append(role)

            await member.move_to(room)
            await member.add_roles(role)



        for _ in range(len(voicechannels) if len(voicechannels) < 3 else 3):
            # How many times to rotate; meaning 2 rotations = 3 conversations
            # Get talk duration from DB
            result = self.bot.db['configs'].find(guild_id=ctx.guild.id)
            results = [r for r in result]
            duration = results[0]['duration'] if len( results ) > 0 else os.environ.get('duration', 300)
            duration = int(duration)

            # Tell first member it's "their" turn
            for vc in voicechannels:
                if len(vc.members) == 0:
                    pass

                elif len(vc.members) == 1:
                    if len(self.waiting_line) > 0:
                        u = self.waiting_line.pop(0)
                        self.users.append(u)
                        newmember = discord.utils.get(ctx.guild.members, id=u)
                        await newmember.move_to(vc)
                        await newmember.add_roles(discord.utils.get(ctx.guild.roles, id=self.roles[voicechannels.index(vc)]))
                        await textchannels[voicechannels.index(vc)].send(f'<@{vc.members[0].id}> kan starte med ordet! Så bytter vi midtveis')
                    else:
                        self.users.remove(vc.members[0].id)
                        self.waiting_line.append(vc.members[0].id)
                        dv = discord.utils.get(ctx.guild.voice_channels, id=defaultvoice)
                        await vc.members[0].move_to(dv)
                        await vc.members[0].send('Du har blitt satt på venteliste')

                elif len(vc.members) >= 2:
                    await textchannels[voicechannels.index(vc)].send(f'<@{vc.members[0].id}> kan starte med ordet! Så bytter vi midtveis')

            await asyncio.sleep(duration/2)

            for vc in voicechannels:
                if len(vc.members) == 0:
                    pass

                elif len(vc.members) == 1:
                    if len(self.waiting_line) > 0:
                        u = self.waiting_line.pop(0)
                        self.users.append(u)
                        newmember = discord.utils.get(ctx.guild.members, id=u)
                        await newmember.move_to(vc)
                        await newmember.add_roles(discord.utils.get(ctx.guild.roles, id=self.roles[voicechannels.index(vc)]))
                        await textchannels[voicechannels.index(vc)].send(f'Dere har bare halve tiden fordi forrige person dro! Øverste i VC kan starte, så bytter dere selv!')
                    else:
                        self.users.remove(vc.members[0].id)
                        self.waiting_line.append(vc.members[0].id)
                        dv = discord.utils.get(ctx.guild.voice_channels, id=defaultvoice)
                        await vc.members[0].move_to(dv)
                        await vc.members[0].send('Du har blitt satt på venteliste')

                elif len(vc.members) >= 2:
                    await textchannels[voicechannels.index(vc)].send(f'<@{vc.members[0].id}> <@{vc.members[1].id}> byttetid!')


            await asyncio.sleep(duration/2)

            for t in textchannels:
                await t.send('10 sekunder igjen!')
            await asyncio.sleep(10)

            for t in textchannels:
                async for msg in t.history(limit=500):
                    await msg.delete()

            # Rotate users
            moved = []
            for i in range(len(voicechannels)):
                vc = voicechannels[i]

                if len(voicechannels[i-1].members) == 0:
                    pass

                elif len(voicechannels[i-1].members) >= 1:
                    # Take the user from the previous voice channel and move them in here
                    for m in voicechannels[i-1].members:
                        if not m.id in moved:
                            for r in self.roles:
                                if r in m.roles:
                                    await m.remove_roles(r)
                            await m.move_to(vc)
                            await m.add_roles(self.roles[voicechannels.index(vc)])
                            break


        # Remove room roles
        for u in self.users:
            for r in self.roles:
                if r in u.roles:
                    await u.remove_roles(r)

        self.users = []
        self.waiting_line = []
        self.running = False

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not after.channel and self.running and member.id in self.users:
            self.users.remove(member.id)

            # Remove the room roles when they leave
            oldr = None
            for r in self.roles:
                if r in member.roles:
                    oldr = r
                    await member.remove_roles(r)

            if len(self.waiting_line) > 0:
                newmember = discord.utils.get(member.guild.members, id=self.waiting_line[0])
                await newmember.move_to(before.channel)
                await newmember.add_roles(oldr)


def setup(bot):
    bot.add_cog(Rotation(bot))
