import discord
from discord.ext import commands
import random
import aiohttp
import time
from main import bot as b

color = 0x2f3136

barks = [
    "Bark!",
    "Arf!",
    "Woof!",
    "Bork!"
]

class pictures(commands.Cog):
    """API Commands to mess with"""
    
    def __init__(self, bot):
        self.bot = b

    @commands.command(description="Woof")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_guild_permissions(embed_links=True)
    async def dog(self,ctx: commands.Context):
        start = time.perf_counter()
        timeout = aiohttp.ClientTimeout(total=4)
        myurl='https://dog.ceo/api/breeds/image/random'
        async with aiohttp.ClientSession(timeout=timeout) as cs:
            async with cs.get(myurl) as rep:
                try:
                    url= await rep.json()
                except Exception as e:
                    if ctx.author.id in self.bot.owner_ids:
                        await ctx.send(
                            f"""
An unexpected error occured:
```py
{e}
```
                            """
                        )
                    elif ctx.author.id not in self.bot.owner_ids:
                        await ctx.send("An unexpected error occured")
        end = time.perf_counter()

        bark = random.choice(barks)
        embed=discord.Embed(
            title=bark,
            color=self.bot.colors["main"]
        )
        embed.set_image(
            url=url["message"]
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url
        )
        await ctx.reply(
            f"{bark} Fetching took `{end - start:.3f}s`",
            embed=embed,
            mention_author=False
        )

    @commands.command(description="Arf!")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_guild_permissions(embed_links=True)
    async def doggo(self,ctx: commands.Context):
        start = time.perf_counter()
        timeout = aiohttp.ClientTimeout(total=4)
        myurl=random.choice(['https://dog.ceo/api/breed/shiba/images/random','https://dog.ceo/api/breed/akita/images/random'])
        async with aiohttp.ClientSession(timeout=timeout) as cs:
            async with cs.get(myurl) as rep:
                try:
                    url= await rep.json()
                except Exception as e:
                    if ctx.author.id in self.bot.owner_ids:
                        await ctx.send(
                            f"""
An unexpected error occured:
```py
{e}
```
                            """
                        )
                    elif ctx.author.id not in self.bot.owner_ids:
                        await ctx.send("An unexpected error occured")
        end = time.perf_counter()

        bark = random.choice(barks)
        embed=discord.Embed(
            title=bark,
            color=self.bot.colors["main"]
        )
        embed.set_image(
            url=url["message"]
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url
        )
        await ctx.reply(
            f"{bark} Fetching took `{end - start:.3f}s`",
            embed=embed,
            mention_author=False
        )

    @commands.command(description="Gets shiba inu image")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_guild_permissions(embed_links=True)
    async def shiba(self,ctx:commands.Context):
        start = time.perf_counter()
        timeout = aiohttp.ClientTimeout(total=4)
        myurl='https://dog.ceo/api/breed/shiba/images/random'
        async with aiohttp.ClientSession(timeout=timeout) as cs:
            async with cs.get(myurl) as rep:
                try:
                    url= await rep.json()
                except Exception as e:
                    if ctx.author.id in self.bot.owner_ids:
                        await ctx.send(
                            f"""
An unexpected error occured:
```py
{e}
```
                            """
                        )
                    elif ctx.author.id not in self.bot.owner_ids:
                        await ctx.send("An unexpected error occured")
        end = time.perf_counter()

        bark = random.choice(barks)
        embed=discord.Embed(
            title=bark,
            color=self.bot.colors["main"]
        )
        embed.set_image(
            url=url["message"]
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url
        )
        await ctx.reply(
            f"{bark} Fetching took `{end - start:.3f}s`",
            embed=embed,
            mention_author=False
        )

    @commands.command(description="Gets akita inu image")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_guild_permissions(embed_links=True)
    async def akita(self,ctx:commands.Context):
        start = time.perf_counter()
        timeout = aiohttp.ClientTimeout(total=4)
        myurl='https://dog.ceo/api/breed/akita/images/random'
        async with aiohttp.ClientSession(timeout=timeout) as cs:
            async with cs.get(myurl) as rep:
                try:
                    url= await rep.json()
                except Exception as e:
                    if ctx.author.id in self.bot.owner_ids:
                        await ctx.send(
                            f"""
An unexpected error occured:
```py
{e}
```
                            """
                        )
                    elif ctx.author.id not in self.bot.owner_ids:
                        await ctx.send("An unexpected error occured")
        end = time.perf_counter()

        bark = random.choice(barks)
        embed=discord.Embed(
            title=bark,
            color=self.bot.colors["main"]
        )
        embed.set_image(
            url=url["message"]
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url
        )
        await ctx.reply(
            f"{bark} Fetching took `{end - start:.3f}s`",
            embed=embed,
            mention_author=False
        )

def setup(bot):
    bot.add_cog(pictures(bot))