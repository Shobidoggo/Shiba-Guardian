from pydoc import describe
import random
from click import command
import discord
from discord.ext import commands
import asyncio
from data import edited_msgs, reactions, afks, dnds, messages
from funcs import count, raw
from main import bot as b
from typing import Union


color = 0x2f3136

class utility(commands.Cog):
    """Useful commands to try out"""

    def __init__(self, bot):
        self.bot = b

    @commands.command(description="Invite the bot to your server!")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def invite(self, ctx: commands.Context):
        await ctx.reply(
            embed=discord.Embed(
                title="Bot Invite",
                description=f"[Click here to add the bot!]({self.bot.invite})",
                color=self.bot.colors["main"]
            ),
            mention_author=False
        )

    @commands.group(name="snipe",invoke_without_command=True,description="Snipe your choosing channel")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def snipe(self, ctx: commands.Context, *, channel : discord.TextChannel = None):
        channel = channel or ctx.channel
        if messages.get(str(channel.id)) != None:
            if channel.nsfw and not ctx.channel.nsfw:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"{self.bot.icons['warning']} **{ctx.author.name}**, this channel needs to be NSFW to snipe messages from NSFW channels",
                        color=self.bot.colors["red"]
                    ),
                    mention_author=False
                )
            msg: discord.Message = messages[str(channel.id)]
            content = "*Message did not contain any content*" if msg.content is None or len(msg.content) == 0 else "```\n"+msg.content.replace("```","`‎`‎`")+"\n```"
            e=discord.Embed(
                description=content,
                color=self.bot.colors["main"]
            )
            e.set_author(
                name=f"{msg.author} ({msg.author.id}) said in #{msg.channel}",
                icon_url=msg.author.avatar.url if msg.author.avatar else None
            )
            if msg.attachments:
                e.set_image(url=msg.attachments[0].url)
            stickers = 0
            stickerCollect = []
            if msg.stickers:
                for sticker in msg.stickers:
                    stickers+=1
                    stickerCollect.append(f"[Sticker {stickers}]({sticker.url} 'Sticker URL')")
                e.add_field(
                    name="Stickers",
                    value=", ".join(stickerCollect),
                    inline=False
                )
            embeds = [e]
            for embed in msg.embeds:
                embeds.append(embed)
            await ctx.reply(
                embeds=embeds,
                mention_author=False
            )
        else:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} **{ctx.author.mention}**, I do not have any sniped messages for {channel.mention}",
                    color=self.bot.colors["red"]
                ),
                mention_author=False
            )

    @snipe.command(description="Snipes an edited message")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def edit(self, ctx: commands.Context, *, channel : discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if edited_msgs.get(str(channel.id)) == None:
            await ctx.reply(
                f"{self.bot.icons['warning']} There are no edited messages to be sniped in {channel.mention}",
                mention_author=False
            )
        else:
            message = edited_msgs.get(str(channel.id))[str("message")]
            before = edited_msgs.get(str(channel.id))["before"]
            content = edited_msgs.get(str(channel.id))["content"]
            author = edited_msgs.get(str(channel.id))["author"]
            if content is None or len(content) == 0:
                 content = "*Message did not contain any content*"
            elif content is not None or len(content) > 0:
                content = content
            if before.content is None or len(before.content) == 0:
                before_content = "*Message did not cointain any content*"
            elif before.content is not None or len(before.content) > 0:
                before_content = before.content
            e=discord.Embed(
                color=self.bot.colors["main"]
            )
            if author.avatar.url is not None:
                e.set_author(
                    name=f"{author} ({author.id}) said in #{message.channel}",
                    icon_url=author.avatar.url
                )
            elif author.avatar.url is None:
                e.set_author(
                    name=f"{author} ({author.id}) said in #{message.channel}"
                )
            if len(before_content) > 1000:
                e.add_field(
                    name="Before",
                    value="Content contained above 1000 characters",
                    inline=False
                )
            elif len(before_content) <= 1000:
                e.add_field(
                    name="Before",
                    value=before_content,
                    inline=False
                )
            if len(content) > 1000:
                e.add_field(
                    name="After",
                    value="Content contained above 1000 characters",
                    inline=False
                )
            elif len(content) <= 1000:
                e.add_field(
                    name="After",
                    value=content,
                    inline=False
                )
            e.add_field(
                name="Message URL",
                value=f"[Click Here]({message.jump_url} 'Message URL')"
            )
            await ctx.reply(
                embed=e,
                mention_author=False
            )
    
    @snipe.command(description="Snipes a removed reaction")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def reaction(self, ctx: commands.Context, *, channel : discord.TextChannel = None):
        channel = channel or ctx.channel
        if reactions.get(str(channel.id)) == None:
            await ctx.reply(
                f"{self.bot.icons['warning']} There are no deleted reactions to be sniped in {channel.mention}",
                mention_author=False
            )
        else:
            msg: discord.Message = reactions.get(str(channel.id))["message"]
            author = reactions.get(str(channel.id))["reaction_author"]
            emoji = reactions.get(str(channel.id))["emoji"]
            emoji_url = reactions.get(str(channel.id))["emoji_url"]
            e=discord.Embed(
                description=f"""
**Emoji:** {emoji}
**Message URL:** [Click here]({msg.jump_url} "Message URL")
                """,
                color=self.bot.colors["main"]
            )
            e.set_author(
                name=f"{author} ({author.id}) reacted in #{channel.name}",
                icon_url=author.avatar.url or None
            )
            e.set_image(
                url=emoji_url
            )
            await ctx.reply(
                embed=e,
                mention_author=False
            )

    @commands.command(description="Gives you AFK mode")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def afk(self, ctx: commands.Context, *, reason = None):
        reason = reason or 'AFK'
        if afks.get(ctx.author.id):
            return await ctx.reply(
                f'{self.bot.icons["warning"]} You are already AFK',
                mention_author=False
            )

        await ctx.reply(
            f"{self.bot.icons['check']} Marked you as AFK: **{reason}**",
            mention_author=False
        )
        await asyncio.sleep(0.1)
        afks[ctx.author.id] = {"reason" : reason}
    
    @commands.group(invoke_without_command=True,description="Gives you DND mode")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dnd(self, ctx: commands.Context):
        await ctx.send_help("dnd")
    
    @dnd.command(aliases=["on"],description="Enables dnd mode for you",)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def enable(self, ctx: commands.Context, *, reason = None):
        if dnds.get(ctx.author.id) != None:
            await ctx.reply(
                f"{self.bot.icons['warning']} Your DND is on",
                mention_author=False
            )
        elif dnds.get(ctx.author.id) == None:
            reason = reason or 'DND'

            await ctx.reply(
                f"{self.bot.icons['check']} Marked you as DND: **{reason}**",
                mention_author=False
            )
            await asyncio.sleep(0.1)
            dnds[ctx.author.id] = {"reason" : reason}
    
    @dnd.command(aliases=["off"],description="Disables DND mode for you")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def disable(self, ctx: commands.Context):
        if not dnds.get(ctx.author.id):
            await ctx.reply(
                f"{self.bot.icons['warning']} Your DND is not enabled",
                mention_author=False
            )
        elif dnds.get(ctx.author.id):
            del dnds[ctx.author.id]
            await ctx.reply(
                f"{self.bot.icons['check']} I have unmarked you as DND",
                mention_author=False
            )

    @commands.command(description="See the very first message of a channel")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def firstmsg(self, ctx: commands.Context, *, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        try:
            async for msg in channel.history(limit=1, oldest_first=True):
                await ctx.reply(
                    embed=discord.Embed(
                        description=f"Click [here]({msg.jump_url} \"First Message URL\") to view the first message of {channel.mention} by **{msg.author}**",
                        color=self.bot.colors["main"]
                    ),
                    mention_author=False
                )
        except discord.Forbidden:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} I do not have permission to view that channel",
                    color=self.bot.colors["red"]
                ),
                mention_author=False
            )
    
    @commands.command(help="Raws a markdown message. Can either be a message or simple markdown")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def raw(self, ctx: commands.Context, *, content: Union[discord.Message, commands.clean_content] = None):
        if content is None and ctx.message.reference:
            content = ctx.message.reference.resolved.content
        elif content is None and not ctx.message.reference:
            return await ctx.send(f'{self.bot.icons["warning"]} You are not replying to a message')
        if isinstance(content, discord.Message): content = content.clean_content
        else: content = content
        await ctx.send(raw(content))
    
    @commands.command(description="Spoilers every letter")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def spoiler(self, ctx: commands.Context, *, message):
        chars = []
        for char in message:
            chars.append(char)
        spoiler = "".join(f"||{c}||" for c in chars)
        e=discord.Embed(color=self.bot.colors["main"])
        e.add_field(
            name="Input",
            value=message,
            inline=False
        )
        e.add_field(
            name="Output",
            value=spoiler,
            inline=False
        )
        return await ctx.reply(
            embed=e,
            mention_author=False
        )
    
    @commands.command(description="Reveals a spoiler")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unspoiler(self, ctx: commands.Context, *, spoiler_message):
        if "||" not in spoiler_message:
            await ctx.reply(
                f"{self.bot.icons['warning']} You need to have a spoiler message to be uncovered!",
                mention_author=False
            )
        else:
            e=discord.Embed(
                title="Spoiler Message",
                color=self.bot.colors["main"]
            )
            e.add_field(
                name="Input",
                value=spoiler_message,
                inline=False
            )
            e.add_field(
                name="Output",
                value=f"```\n{spoiler_message}\n```".replace("||", ""),
                inline=False
            )
            await ctx.reply(
                embed=e,
                mention_author=False
            )
    
    @commands.command(description="Chooses a choice for you")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def choose(self, ctx: commands.Context, *, choices):
        choice_data = []
        for choice in f"{choices}".split(","):
            choice_data.append(choice)
        
        await ctx.reply(
            random.choice(choice_data),
            mention_author=False
        )

    @commands.group(name="avatar",aliases=["av", "pfp", "profile", "icon"],description="Gives you the avatar link of a member",invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def av(self, ctx: commands.Context):
        await ctx.send_help(ctx.command.qualified_name)
    
    @av.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def guild(self, ctx: commands.Context, member : discord.Member = None):
        member = member or ctx.author
        if not member.guild_avatar:
            return await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} This member does not have a guild avatar for this guild",
                    color=self.bot.colors["red"]
                ),
                mention_author=False
            )
        
        avatar_png = member.guild_avatar.with_format("png").url
        avatar_jpg = member.guild_avatar.with_format("jpg").url
        avatar_jpeg = member.guild_avatar.with_format("jpeg").url
        avatar_webp = member.guild_avatar.with_format("jpeg").url
        if member.guild_avatar.is_animated():
            avatar_gif = member.guild_avatar.with_format("gif").url
        if member.guild_avatar.is_animated():
            em=discord.Embed(
                title=f"{member} avatar",
                description=f"**[PNG]({avatar_png}) | [JPG]({avatar_jpg}) | [JPEG]({avatar_jpeg}) | [WEBP]({avatar_webp}) | [GIF]({avatar_gif})**",
                color=self.bot.colors["main"]
            )
        else:
            em=discord.Embed(
                title=f"{member} avatar",
                description=f"[PNG]({avatar_png}) | [JPG]({avatar_jpg}) | [JPEG]({avatar_jpeg}) | [WEBP]({avatar_webp})",
                color=self.bot.colors["main"]
            )
        em.set_image(
            url=member.guild_avatar.url
        )
        await ctx.reply(
            embed=em,
            mention_author=False
        )
    
    @av.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def normal(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        if not member.avatar:
            return await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} This member does not an avatar",
                    color=self.bot.colors["red"]
                ),
                mention_author=False
            )

        avatar_png = member.avatar.with_format("png").url
        avatar_jpg = member.avatar.with_format("jpg").url
        avatar_jpeg = member.avatar.with_format("jpeg").url
        avatar_webp = member.avatar.with_format("jpeg").url
        if member.avatar.is_animated():
            avatar_gif = member.avatar.with_format("gif").url
        if member.avatar.is_animated():
            em=discord.Embed(
                title=member.name+"'s avatar",
                description=f"**[PNG]({avatar_png}) | [JPG]({avatar_jpg}) | [JPEG]({avatar_jpeg}) | [WEBP]({avatar_webp}) | [GIF]({avatar_gif})**",
                color=self.bot.colors["main"]
            )
        else:
            em=discord.Embed(
                title=member.name+"'s avatar",
                description=f"[PNG]({avatar_png}) | [JPG]({avatar_jpg}) | [JPEG]({avatar_jpeg}) | [WEBP]({avatar_webp})",
                color=self.bot.colors["main"]
            )
        em.set_image(
            url=member.avatar.url
        )
        await ctx.reply(
            embed=em,
            mention_author=False
        )
    
    @av.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def banner(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        member = await self.bot.fetch_user(member.id)
        if not member.banner:
            return await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} This member does not a banner",
                    color=self.bot.colors["red"]
                ),
                mention_author=False
            )

        avatar_png = member.banner.with_format("png").url
        avatar_jpg = member.banner.with_format("jpg").url
        avatar_jpeg = member.banner.with_format("jpeg").url
        avatar_webp = member.banner.with_format("jpeg").url
        if member.banner.is_animated():
            avatar_gif = member.banner.with_format("gif").url
        if member.banner.is_animated():
            em=discord.Embed(
                title=f"{member} banner",
                description=f"**[PNG]({avatar_png}) | [JPG]({avatar_jpg}) | [JPEG]({avatar_jpeg}) | [WEBP]({avatar_webp}) | [GIF]({avatar_gif})**",
                color=self.bot.colors["main"]
            )
        else:
            em=discord.Embed(
                title=f"{member} banner",
                description=f"[PNG]({avatar_png}) | [JPG]({avatar_jpg}) | [JPEG]({avatar_jpeg}) | [WEBP]({avatar_webp})",
                color=self.bot.colors["main"]
            )
        em.set_image(
            url=member.banner.url
        )
        await ctx.reply(
            embed=em,
            mention_author=False
        )

    @commands.command(name="binary",description="converts your text into binary")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def binary(self, ctx: commands.Context, *, text: str):
        converter = bytearray(text, "utf8")

        output = []

        for byte in converter:
            binary_representation = bin(byte)
            output.append(binary_representation.replace("b",""))

        e=discord.Embed(
            title="Binary Converter",
            color=self.bot.colors["main"]
        )
        e.add_field(
            name="Input",
            value=text,
            inline=False
        )
        e.add_field(
            name="Output",
            value=" ".join(str(num) for num in output),
            inline=False
        )
        return await ctx.reply(
            embed=e,
            mention_author=False
        )

def setup(bot):
    bot.add_cog(utility(bot))