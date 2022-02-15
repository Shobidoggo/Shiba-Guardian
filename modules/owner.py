from dataclasses import astuple
from typing import Union
from discord import embeds
from discord.ext.commands.core import command
from discord.ext.commands.errors import ExtensionNotLoaded, UserInputError
from discord.ext.commands.flags import F
import discord
from discord.ext import commands
import random
import asyncio
from main import bot as b
from jishaku.codeblocks import codeblock_converter

color = 0x2f3136

class owner(commands.Cog):
    """commands for the bot developers only"""

    def __init__(self, bot):
        self.bot = b
    
    @commands.command(description="Deletes a message")
    @commands.is_owner()
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def sdel(self, ctx: commands.Context, *, message : discord.Message):
        try:
            await message.delete()
            try:
                await ctx.author.send(self.bot.icons['check'])
            except:
                return
        except:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} **{ctx.author.name}**, I do not have permission to delete that message",
                    color=self.bot.colors["red"]
                ),
                mention_author=False
            )
    
    @commands.command(description="DM a user")
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.is_owner()
    async def dmsend(self, ctx: commands.Context, user : Union[discord.Member, discord.User], *, message):
        try:
            e=discord.Embed(
                description=message,
                color=self.bot.colors["main"]
            )
            e.set_author(
                name=f"{ctx.author} | {ctx.author.id}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )
            await user.send(
                embed=e
            )
            return await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['check']} I have sent **{user} ({user.id})** the message",
                    color=self.bot.colors["main"]
                ),
                mention_author=False
            )
        except:
            return await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} I do not have permission to DM this user",
                    color=self.bot.colors["red"]
                ),
                mention_author=False
            )

    @commands.command(description="Replies to your choosing of messages")
    @commands.is_owner()
    async def sendmsg(self, ctx: commands.Context, message : discord.Message, *, custom_message):
        try:
            if message.channel == ctx.channel:
                await message.reply(
                    custom_message,
                    mention_author=False
                )
            else:
                await message.reply(
                    custom_message,
                    mention_author=False
                )
                await ctx.send(self.bot.icons["check"])
        except:
            await ctx.send('Couldn\'t reply to that message')

    @commands.command(aliases=["r"],description="Reload an extension or more")
    @commands.cooldown(1, 6, commands.BucketType.user)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, extensions : str):
        if extensions.lower() == "all":
            extensions = " ".join(ext for ext in self.bot.extensions)
        data = []
        for ext in f"{extensions}".split():
            data.append(ext)
        exts = []
        for ext in data:
            try:
                self.bot.reload_extension(ext)
                exts.append(f"🔁 `{ext}`")
            except Exception as e:
                exts.append(f"{self.bot.icons['warning']} `{ext}` - {e}")
        
        await ctx.reply(
            "\n\n".join(exts),
            mention_author=False
        )

    @commands.command(description="Shuts down the bot")
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context):
        msg = await ctx.reply(
            "I am now going offline in 3...",
            mention_author=False
        )
        await asyncio.sleep(1)
        await msg.edit(content="I am now going offline in 2...")
        await asyncio.sleep(1)
        await msg.edit(content="I am now going offline in 1...")
        await asyncio.sleep(1)
        await msg.edit(content="I am now going offline in 0...")
        await asyncio.sleep(0.5)
        await msg.edit(content=self.bot.icons["check"])
        await self.bot.close()

def setup(bot):
    bot.add_cog(owner(bot))