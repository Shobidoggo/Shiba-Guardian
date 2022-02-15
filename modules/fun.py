from collections import namedtuple
from typing import Union
import discord
from discord.ext import commands
import random
import asyncio
import asyncio
import base64
import datetime
import string
import time
from funcs import count
from main import bot as b

guild_ids = [697068320133742642, 336642139381301249]
color = 0x2f3136

class fun(commands.Cog):
    """Fun commands to mess around with!"""

    def __init__(self, bot):
        self.bot = b
    
    @commands.command(description="Does a poll for you",)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def poll(self, ctx: commands.Context, *, poll):
        if "\n" not in poll:
            e=discord.Embed(
                title=f"**{poll}**",
                color=self.bot.colors["main"]
            )
            e.set_author(
                name="Poll",
                icon_url=ctx.author.avatar.url
            )
            msg = await ctx.send(embed=e)
            try:
                await msg.add_reaction("👍")
                await msg.add_reaction("👎")
            except:
                return
        elif "\n" in poll:
            poll_data = []
            for line in f"{poll}".split("\n"):
                poll_data.append(line)
            if len(poll_data) > 6:
                e=discord.Embed(
                    description=f"",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(
                    f"{self.bot.icons['warning']} You can not have more than 6 lines in your poll",
                    mention_author=False
                )
            else:
                e=discord.Embed(
                    title=f"**{poll_data[0]}**",
                    description="\n".join(line for line in poll_data[1:6]),
                    color=self.bot.colors["main"]
                )
                msg = await ctx.send(embed=e)
                try:
                    if len(poll_data) == 2:
                        await msg.add_reaction("1️⃣")
                    elif len(poll_data) == 3:
                        await msg.add_reaction("1️⃣")
                        await msg.add_reaction("2️⃣")
                    elif len(poll_data) == 4:
                        await msg.add_reaction("1️⃣")
                        await msg.add_reaction("2️⃣")
                        await msg.add_reaction("3️⃣")
                    elif len(poll_data) == 5:
                        await msg.add_reaction("1️⃣")
                        await msg.add_reaction("2️⃣")
                        await msg.add_reaction("3️⃣")
                        await msg.add_reaction("4️⃣")
                    elif len(poll_data) == 6:
                        await msg.add_reaction("1️⃣")
                        await msg.add_reaction("2️⃣")
                        await msg.add_reaction("3️⃣")
                        await msg.add_reaction("4️⃣")
                        await msg.add_reaction("5️⃣")
                except:
                    return

    @commands.command(name="8ball",description="Ask any question!")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _8ball(self, ctx: commands.Context, *, question):
        choices = [
            "Yes",
            "No",
            "I don't know",
            "I'm not too sure",
            "Probably",
            "Probably not",
            "Most likely",
            "Most likely not",
            "Maybe",
            "Maybe not",
            "Obviously",
            "Obviously not",
            "Not really",
            "Absolutely",
            "Absolutely not",
            "There's a possibility"
        ]
        if len(question) > 250:
            await ctx.reply(
                f"{self.bot.icons['warning']} Your question cannot be longer than 250 characters!",
                mention_author=False
            )
        elif len(question) <= 250:
            await ctx.reply(
                f"""
**Question:** {question}
**Answer:** {random.choice(choices)}
                """,
                mention_author=False
            )
    
    @commands.command(help="Quote your own message")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def quote(self, ctx: commands.Context, *, quote: str = None):
        if ctx.message.reference:
            if ctx.message.reference.resolved:
                msg = ctx.message.reference.resolved
                return await ctx.send(
                    f"\"{msg.clean_content}\"- {msg.author.name}, 2022",
                    allowed_mentions=discord.AllowedMentions.none()
                )
        if not quote and not ctx.message.reference:
            return await ctx.send_help(ctx.command.qualified_name)
        return await ctx.send(
            f'"{quote}"- {ctx.author.name if not ctx.author.nick else ctx.author.nick}, 2022',
            allowed_mentions=discord.AllowedMentions.none()
        )
    
    @commands.command(name="rps",aliases=["rockpaperscissors"],description="can you beat the bot?",help="!rps rock")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rps(self, ctx: commands.Context, *, choices: str):
        valid = []
        valid_choices = ["rock", "paper", "scissors"]
        Random = {
            1: ["rock", "paper", "scissors"],
            2: ["rock", "paper", "scissors"],
            3: ["rock", "paper", "scissors"]
        }
        emojis = {"rock": "🪨", "paper": "📜","scissors": "✂"}
        for type in choices.lower().split():
            if type in valid_choices:
                valid.append(type)
        if valid:
            if count(valid) > 3:
                return await ctx.send('You can\'t send more than 3 choices at once')
            num = 0
            for choice in valid:
                num+=1
                ai_choice = random.choice(Random[num])
                status = None
                if choice == ai_choice:
                    status = f"Tie!"
                elif choice.lower() == "rock" and ai_choice == "scissors":
                    status = "You win!"
                elif choice == "paper" and ai_choice == "rock":
                    status = "You win!"
                elif choice == "scissors" and ai_choice == "paper":
                    status = "You win!"
                else:
                    status = "AI wins!"
                e=discord.Embed(
                    title="Rock, Paper, Scissors!",
                    description=status,
                    color=self.bot.colors["main"]
                )
                e.add_field(
                    name="Your Choice",
                    value=f"{emojis[choice]} {choice}".title()
                )
                e.add_field(
                    name="AI's Choice",
                    value=f"{emojis[ai_choice]} {ai_choice}".title()
                )
                e.set_image(
                    url="https://cdn.discordapp.com/attachments/919620192915574814/925778559753138226/RPS_Banner.gif"
                )
                await ctx.send(embed=e)
        else:
            await ctx.send('None of your choices are valid!')
    
    @commands.command(aliases=["tr"],description="With modes of 'easy', 'medium', 'hard', and 'extreme'")
    @commands.cooldown(1, 40, commands.BucketType.channel)
    async def typeracer(self, ctx, mode : str = None):
        valid_modes = "easy medium hard extreme".split()
        if mode is None:
            mode = "easy"
            seconds = 4
        elif mode.lower() in valid_modes and mode is not None:
            if mode.lower() == "easy":
                mode = "easy"
                seconds = 4
            elif mode.lower() == "medium":
                mode = "medium"
                seconds = 2
            elif mode.lower() == "hard":
                mode = "hard"
                seconds = 1
            elif mode.lower() == "extreme":
                mode = "extreme"
                seconds = 0.5
        else:
            return await ctx.send(embed=discord.Embed(title=f"{self.bot.icons['warning']} | Invalid Mode",description=f"Valid Modes: "+", ".join(f"`{m}`" for m in valid_modes),color=self.bot.colors["red"]))

        easy = "hi a you hey what got mum low ice cool cow fun the dog king".split()
        medium = "your mouse computer curtain window door object high frame photo".split()
        hard = "helicopter computer monitor picture-frame prison escape atlantic suspicious".split()
        extreme = "suspicious-ness circumstance exhaustful momentum physics helicopter air-drive hard-drive sexual courses".split()
        if mode.lower() == "easy":
            words = easy
            amount = random.randint(5,10)
        elif mode.lower() == "medium":
            words = medium
            amount = random.randint(12,17)
        elif mode.lower() == "hard":
            words = hard
            amount = random.randint(20,30)
        elif mode.lower() == "extreme":
            words = extreme
            amount = random.randint(25,40)

        sentence_data = []
        for x in range(amount):
            sentence_data.append(random.choice(words))

        sentenceAns = " ".join(sentence_data)
        sentence = " ".join(sentence_data).replace("u","ս").replace("o","օ")

        def check(m : discord.Message):return m.content.lower() == sentenceAns and m.channel == ctx.channel

        await ctx.send(
            embed=discord.Embed(
                title=f"Mode: {mode} ({seconds} seconds per word)".lower().title(),
                description=f"""
```
{sentence}
```
                """,
                color=self.bot.colors["main"]
            )
        )
        timeout = int(len(sentenceAns.split()))*seconds

        start = time.perf_counter()
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=timeout)
        except asyncio.TimeoutError:
            if mode == "easy":
                return await ctx.send(
                    embed=discord.Embed(
                        title=f"{self.bot.icons['cross']} | Timeout",
                        description=f"No one got above 15 WPM (`{timeout}s`)",
                        color=self.bot.colors["red"]
                    )
                )
            elif mode == "medium":
                return await ctx.send(
                    embed=discord.Embed(
                        title=f"{self.bot.icons['cross']} | Timeout",
                        description=f"No one got above 30 WPM (`{timeout}s`)",
                        color=self.bot.colors["red"]
                    )
                )
            elif mode == "hard":
                return await ctx.send(
                    embed=discord.Embed(
                        title=f"{self.bot.icons['cross']} | Timeout",
                        description=f"No one got above 60 WPM (`{timeout}s`)",
                        color=self.bot.colors["red"]
                    )
                )
            elif mode == "extreme":
                return await ctx.send(
                    embed=discord.Embed(
                        title=f"{self.bot.icons['cross']} | Timeout",
                        description=f"No one got above 120 WPM",
                        color=self.bot.colors["red"]
                    )
                )
        else:
            end = time.perf_counter()
            spare_time = timeout - int(end - start)
            await msg.add_reaction("🥇")
            wpm = len(sentenceAns.split())/(int(end - start)/60)
            return await ctx.send(
                embed=discord.Embed(
                    title="🥇",
                    description=f"""
**Winner:** {msg.author}
**Duration:** `{int(end - start)}s`
**Spare Time:** `{spare_time}s`
**WPM:** `{int(wpm)}`
                    """,
                    color=self.bot.colors["main"]
                )
            )
    
    @commands.command(description="Make an embed; example: grey This is the title | this is the description")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def embed(self, ctx: commands.Context, color : Union[discord.Color, str], *, embed):
        data = []
        for param in f"{embed}".split("|"):
            data.append(param)
        if len(data) < 2 or len(data) > 2:
            return await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} **{ctx.author.name}**, you seem to have incorrectly executed this command, use `{ctx.prefix}help {ctx.command.qualified_name}` for help",
                    color=self.bot.colors["red"]
                ),
                mention_author=False
            )
        try:
            return await ctx.send(
                embed=discord.Embed(
                    title=data[0],
                    description=data[1],
                    color=color
                )
            )
        except:
            return await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} **{ctx.author.name}**, you seem to have incorrectly executed this command, use `{ctx.prefix}help {ctx.command.qualified_name}` for help",
                    color=self.bot.error
                ),
                mention_author=False
            )

    @commands.command(name="ship",description="see people's love percentages!",help="!ship @Shobi @NotFahad")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ship(self, ctx: commands.Context, first_user : discord.Member, second_user : discord.Member = None):
        second_user = second_user or ctx.author
        if first_user.id == second_user.id:
            await ctx.reply(
                f"{self.bot.icons['cross']} The first user cannot be the same to the second user",
                mention_author=False
            )
            return
        ship_percentage = random.randint(0,100)
        if ship_percentage <= 30:
            message = "I don't see a sign of love here"
        elif ship_percentage >= 31 and ship_percentage < 49:
            message = "Something could be sparking!"
        elif ship_percentage >= 50 and ship_percentage <= 70:
            message = "This love could be strong!"
        elif ship_percentage >= 71 and ship_percentage <= 99:
            message = "I think this love will work"
        elif ship_percentage == 100:
            message = "They're getting married!!"
        await ctx.reply(
            f"{self.bot.icons['heart']} **{first_user.name}** & **{second_user.name}** are {ship_percentage}% compatible!\n{message}",
            mention_author=False
        )
    
    @commands.command(name="robloxchat",description="gives you a roblox chat including chat filter and username filter",help="/robloxchat Hello. This is the roblox chat")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def robloxchat(self, ctx: commands.Context, *, message: str):
        filter = [
            "fuck","shit","fucker","bullshit","fucking","bull-shit",
            "nigger","nigga","cum","ass","wtf","tf","mf","motherfucker",
            "mother-fucker","dick","cock","penis","pussy","vagina",
            "masturbate","masturbation","masturbating","ejaculate",
            "ejaculation","ejaculating","bitch","cunt","bastard",
            "hoe","whore","fag","faggot","stfu","dumbass","idiot",
            "stupid"
        ]
        userName = []
        chars = []
        content = []
        for char in string.ascii_letters+string.digits:
            chars.append(char)
        for char in ctx.author.name:
            if char in chars:
                userName.append(char)
        for key in message.split():
            if key.lower() in filter:
                content.append("#"*count(key))
            else:
                content.append(key)
        
        robloxUser = f"[{''.join(userName)}]: "
        content = ' '.join(content).replace("# #","#"*3)
        return await ctx.reply(
            embed=discord.Embed(
                title="Roblox Chat (Filter Included)",
                description=f"```{robloxUser}{content}```",
                color=self.bot.colors["main"]
            ),mention_author=False
        )
    
    @commands.command(description="Hacks a member's token")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def hacktoken(self, ctx: commands.Context, *, member : discord.Member = None):
        member = member or ctx.author

        # the first part of the token
        byte_first = str(member.id).encode('ascii')
        first_encode = base64.b64encode(byte_first)
        first = first_encode.decode('ascii')
        
        # the middle part of the token
        time_rn = datetime.datetime.utcnow()
        epoch_offset = int(time_rn.timestamp())
        bytes_int = int(epoch_offset).to_bytes(10, "big")
        bytes_clean = bytes_int.lstrip(b"\x00")
        unclean_middle = base64.standard_b64encode(bytes_clean)
        middle = unclean_middle.decode('utf-8').rstrip("==")

        # the last part of the token
        Pair = namedtuple("Pair", "min max")
        num = Pair(48, 57)  # 0 - 9
        cap_alp = Pair(65, 90)  # A - Z
        cap = Pair(97, 122)  # a - z
        select = (num, cap_alp, cap)
        last = ""
        for each in range(27):
            pair = random.choice(select)
            last += str(chr(random.randint(pair.min, pair.max)))

        token = ".".join((first, middle, last))
        e=discord.Embed(
            title="token hack completed".title(),
            description=f"""
**User:** {member}
**ID:** {member.id}
**Bot:** {self.bot.icons["check"] if member.bot else self.bot.icons["cross"]}
**Time Created:** {discord.utils.format_dt(ctx.message.created_at, "F")}
**Token:** {token}
            """,
            color=self.bot.colors["main"]
        )
        e.set_thumbnail(
            url=member.avatar.url
        )
        await asyncio.sleep(1)
        return await ctx.reply(
            embed=e,
            mention_author=False
        )
    
    @commands.command(description="Hack someone's password")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hackpassword(self, ctx: commands.Context, *, user : Union[discord.Member, discord.User] = None):
        user = user or ctx.author

        data = ["!","\"","£","$","%","^","&","*","(",")","-","_","+","=","|","¬"]
        for char in string.ascii_letters + string.digits:
            data.append(char)
        password = []
        for x in range(random.randint(8,20)):
            password.append(random.choice(data))
        
        final = ''.join(password)

        e=discord.Embed(
            title="password hack complete".title(),
            description=f"""
**User:** {user}
**ID:** {user.id}
**Bot:** {self.bot.icons["check"] if user.bot else self.bot.icons["cross"]}
**Password ({len(final)}):** {final}
            """,
            color=self.bot.colors["main"]
        )
        return await ctx.reply(
            embed=e,
            mention_author=False
        )
    
    @commands.command(description="Please don't die on me")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def battery(self, ctx: commands.Context, *, member : discord.Member = None):
        if member is None:
            member = ctx.author
        
        per = random.randint(0,100)

        e=discord.Embed(
            title=f"{member.name}'s Battery Percentage",
            description=f"**{member.name}'s** battery is currently on {per}%",
            color=self.bot.colors["main"]
        )
        await ctx.reply(
            embed=e,
            mention_author=False
        )
    
    @commands.command(description="No one's beaten my PP size!")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ppsize(self, ctx: commands.Context, *, member : discord.Member = None):
        member = member or ctx.author
        pp = "="
        ran = random.randint(0,46)
        await ctx.reply(
            f"**{member.name}**'s pp size is 8{pp*ran}D",
            mention_author=False
        )
    
    @commands.command(description="make the bot say random stuff",help="!say im a really epic bot")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def say(self, ctx: commands.Context, *, message):
        if len(message) > 500:
            return await ctx.send(
                f"{self.bot.icons['warning']} I cannot send a message with more than 500 characters",
                mention_author=False
            )
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(
            message,
            allowed_mentions=discord.AllowedMentions.none()
        )
        print(f'{ctx.author} made {self.bot.user.name} say "{message}" in {ctx.guild.name} in #{ctx.channel.name}')

    @commands.command(description="Totally real IP")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hackip(self, ctx: commands.Context, *, member : discord.Member = None):
        member = member or ctx.author
        
        ip = f"{random.randint(0,200)}.{random.randint(0,200)}.{random.randint(0,200)}.{random.randint(0,200)}"

        await ctx.reply(
            f"**{member.name}**'s IP is: `{ip}`",
            mention_author=False
        )

def setup(bot):
    bot.add_cog(fun(bot))