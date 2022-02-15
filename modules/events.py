import discord
from discord import emoji
from discord import channel
from discord.ext import commands
from discord.ext.commands import bot
from main import bot as b
import re
import random
import asyncio
from data import messages, edited_msgs, reactions, afks, dnds

class events(commands.Cog):

    def __init__(self, bot):
        self.bot = b
    
    @commands.Cog.listener(name="on_guild_join")
    async def invite_message(self, guild : discord.Guild):
        chan = random.choice(guild.text_channels)
        e=discord.Embed(
            title="Thanks for inviting me!",
            description="""
Hey there! Thanks for inviting me!
If you need any help, just type `v;help`
            """,
            color=self.bot.colors["main"]
        )
        try:
            await chan.send(embed=e)
        except discord.Forbidden:
            return
    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if edited_msgs.get(str(after.channel.id)) == None:
            edited_msgs[str(after.channel.id)] = {}
        if before.content == after.content:
            return
        edited_msgs[str(after.channel.id)][str("message")] = after
        edited_msgs[str(after.channel.id)]["before"] = before
        edited_msgs[str(after.channel.id)]["content"] = after.content
        edited_msgs[str(after.channel.id)]["author"] = after.author
        edited_msgs[str(after.channel.id)]["time_edited"] = discord.utils.format_dt(after.created_at, "R")
            

    @commands.Cog.listener()
    async def on_message_delete(self, msg : discord.Message):
        if messages.get(str(msg.channel.id)) == None:
            messages[str(msg.channel.id)] = {}
        messages[str(msg.channel.id)] = msg
    
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if afks.get(msg.author.id) != None:
            del afks[msg.author.id]
            m = await msg.reply(
                f"{msg.author.mention} I have unmarked you as AFK",
                allowed_mentions=discord.AllowedMentions.none()
            )
            await asyncio.sleep(5)
            await m.delete()

        for user in msg.mentions:
            if afks.get(user.id) != None:
                reason = afks.get(user.id)["reason"]
                await msg.reply(
                    f"<:blobping:923605835542835242> {user.mention} is AFK for: **{reason}**",
                    allowed_mentions=discord.AllowedMentions.none()
                )
            elif dnds.get(user.id) != None:
                reason = dnds.get(user.id)["reason"]
                await msg.reply(
                    f"<:blobping:923605835542835242> {user.mention} is DND for: **{reason}**",
                    allowed_mentions=discord.AllowedMentions.none()
                )
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if reactions.get(str(payload.channel_id)) == None:
            reactions[str(payload.channel_id)] = {}
        channel = self.bot.get_channel(payload.channel_id)
        user = self.bot.get_user(payload.user_id)
        reactions[str(payload.channel_id)]["message"] = channel.get_partial_message(payload.message_id)
        reactions[str(payload.channel_id)]["reaction_author"] = user
        reactions[str(payload.channel_id)]["emoji"] = payload.emoji
        reactions[str(payload.channel_id)]["emoji_url"] = payload.emoji.url
    
    @commands.Cog.listener(name="on_message")
    async def get_prefix(self, msg: discord.Message):
        if msg.content.lower() == f"<@!{self.bot.user.id}>":
            if msg.author.id in self.bot.owner_ids:
                return await msg.reply(
                    'My prefixes are `v;`, ` `',
                    mention_author=False
                )
            return await msg.reply(
                'My prefixes are `v;`',
                mention_author=False
            )

def setup(bot:b):
    bot.add_cog(events(bot))