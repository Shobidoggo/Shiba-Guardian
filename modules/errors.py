import discord
from discord.ext import commands
from main import bot as b
import humanize

class errors(commands.Cog):

    def __init__(self, bot):
        self.bot = b

    @commands.Cog.listener(name="on_command_error")
    async def error_system(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            trigs = [f"{ctx.prefix}{ctx.command.qualified_name}"]
            for cmd in ctx.command.aliases:
                trigs.append(f"{ctx.prefix}{cmd}")
            if ctx.message.content.lower() in trigs:
                return await ctx.send_help(ctx.command.qualified_name)
            arg = error.param.name.replace("_", " ")
            cmd = ctx.invoked_with
            e=discord.Embed(
                description=self.bot.icons["warning"]+f" You forgot the `{arg}` parameter while using `{ctx.prefix}{cmd}`",
                color=self.bot.colors["red"]
            )
            await ctx.reply(
                embed=e,mention_author=False
            )
        elif isinstance(error, commands.CommandOnCooldown):
            e=discord.Embed(
                description=f"{self.bot.icons['warning']} **{ctx.author.name}**, this command is on cooldown. Try again in `{humanize.precisedelta(error.retry_after)}`",
                color=self.bot.colors["red"]
            )
            return await ctx.reply(
                embed=e,mention_author=False
            )
        elif isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MemberNotFound):
                e=discord.Embed(
                    description=self.bot.icons["warning"]+"  Member not found, make sure to check your spelling",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(
                    embed=e,mention_author=False
                )
                return
            if isinstance(error, commands.EmojiNotFound):
                e=discord.Embed(
                    description=self.bot.icons["warning"]+"  That emoji is not in any of my guilds",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(
                    embed=e,mention_author=False
                )
                return
            if isinstance(error, commands.ChannelNotFound):
                e=discord.Embed(
                    description=self.bot.icons["warning"]+" Channel not found",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(
                    embed=e,mention_author=False
                )
                return
            if isinstance(error, commands.RoleNotFound):
                e=discord.Embed(
                    description=self.bot.icons["warning"]+" Role not found",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(
                    embed=e,mention_author=False
                )
                return
            if isinstance(error, commands.UserNotFound):
                e=discord.Embed(
                    description=self.bot.icons["warning"]+" User not found",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(
                    embed=e,mention_author=False
                )
                return
            if isinstance(error, commands.TooManyArguments):
                e=discord.Embed(
                    description=f"{self.bot.icons['warning']} Too many arguments passed",
                    color=self.bot.colors["main"]
                )
                return await ctx.reply(embed=e,mention_author=False)
            cmd = ctx.invoked_with
            e=discord.Embed(
                description=self.bot.icons["warning"]+f" You seem to have incorrectly executed this command, try `{ctx.prefix}help {cmd}` for more info",
                color=self.bot.colors["red"]
            )
            await ctx.reply(
                embed=e,mention_author=False
            )

        elif isinstance(error, commands.MissingPermissions):
            perms = ", ".join(f"`{perm}`".replace("_", " ").title() for perm in error.missing_permissions)
            e=discord.Embed(
                description=self.bot.icons["warning"]+f" You are missing {perms} permission to execute that command",
                color=self.bot.colors["red"]
            )
            await ctx.reply(
                embed=e,mention_author=False
            )
        
        elif isinstance(error, commands.BotMissingPermissions):
            perms = ", ".join(f"`{perm}`".replace("_", " ").title() for perm in error.missing_permissions)
            e=discord.Embed(
                description=self.bot.icons["warning"]+f" I am missing {perms} permission to execute that command",
                color=self.bot.colors["red"]
            )
            await ctx.reply(
                embed=e,mention_author=False
            )

        elif isinstance(error, commands.NotOwner):
            e=discord.Embed(
                description=self.bot.icons["warning"]+"  You are not the owner of this bot",
                color=self.bot.colors["red"]
            )
            await ctx.reply(
                embed=e,mention_author=False
            )

        elif isinstance(error, commands.NSFWChannelRequired):
            e=discord.Embed(
                description=self.bot.icons["warning"]+"  This channel needs to be NSFW for me to execute that command",
                color=self.bot.colors["red"]
            )
            e.set_image(
                url="https://images-ext-2.discordapp.net/external/hiWbEzhiEXfFaza5khoxg3mR3OWeugZwWo8vGxK8LzA/https/i.imgur.com/oe4iK5i.gif"
            )
            await ctx.reply(
                embed=e,mention_author=False
            )
        else:
            if ctx.author.id in self.bot.owner_ids:
                if isinstance(error, commands.CommandNotFound):
                    return
                e=discord.Embed(
                    title=f"{self.bot.icons['warning']} Error",
                    description=f"""
```py
{error}
```
                    """,
                    color=self.bot.colors["red"]
                )
                await ctx.reply(
                    embed=e,mention_author=False
                )
            else:
                if isinstance(error, commands.CommandNotFound) or isinstance(error, discord.Forbidden):
                    return
                await ctx.reply(
                    embed=discord.Embed(
                        description=f"{self.bot.icons['warning']} **{ctx.author.name}**, an error has occured with the bot. I have sent it to my staff team",
                        color=self.bot.colors["red"]
                    ),mention_author=False
                )
                logs = self.bot.get_channel(877495308643344414)
                await logs.send(
                    embed=discord.Embed(
                        title=f"{self.bot.icons['warning']} | Error",
                        description=error,
                        color=self.bot.colors["red"]
                    )
                )

def setup(bot:b):
    bot.add_cog(errors(bot))