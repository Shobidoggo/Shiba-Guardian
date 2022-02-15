# all the imports
import discord
from discord.ext import commands
import os
import aiohttp
import asyncio
import humanize
import string
import funcs
import jishaku
from TOKEN import token

from discord.ext import menus
from discord.ext.menus.views import ViewMenuPages

# bot system

class Shoni(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = aiohttp.ClientSession()
        self.invite = "https://discord.com/api/oauth2/authorize?client_id=936958032590549062&permissions=8&scope=bot"
        self.icons = {
           "check": "✅",
           "cross": "❎",
           "warning": "⚠",
           "arrow": "➡",
           "heart": "❤"
        }
        self.colors = {
            "main" : discord.Color.teal(),
            "red": discord.Color.dark_red(),
            "error": discord.Color.dark_red()
        }

    def say(message : str, repeat : int = 1):
        return (message+"\n")*repeat

owners = [684108370034425925, 692465059695165491]

def pre(bot, msg:discord.Message):
    if msg.author.id in owners:
        return "v;",""
    return "v;"

bot = Shoni(
    command_prefix=pre,
    intents=discord.Intents.all(),
    case_insensitive=True,
    strip_after_prefix=True,
    owner_ids=owners,
    activity=discord.Game("v;help")
)

# jsk system

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

# load cogs

cogs = [
    "jishaku","modules.pictures","modules.fun",
    "modules.info","modules.moderation","modules.owner",
    "modules.utility","modules.errors","modules.events"
]
cogs_statuses = {}

for cog in cogs:
    try:
        bot.load_extension(cog)
        cogs_statuses[cog] = "Loaded"
    except Exception as e:
        print(e)
        cogs_statuses[cog] = e
    
for cog, status in cogs_statuses.items():
    print(f"{cog} - {status}")

# help command

class Help(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        ctx = self.context
        e=discord.Embed(
            title=f"{bot.user.name} help".title(),
            description=f"{ctx.clean_prefix}help [command | module]",
            color=bot.colors["main"]
        )

        for cog in bot.cogs:
            cog = bot.get_cog(cog)
            cmds = await self.filter_commands(cog.get_commands())
            if len(cmds) > 0:
                e.add_field(
                    name=f"{cog.qualified_name}".title(),
                    value="> "+", ".join(f'`{cmd.qualified_name}`' for cmd in cmds),
                    inline=False
                )
        await ctx.send(embed=e)

    async def send_cog_help(self, cog):
        ctx = self.context
        cmds = await self.filter_commands(cog.get_commands())
        e=discord.Embed(
            title=f"(M) {cog.qualified_name.lower()} help".title(),
            description=cog.description if cog.description else 'No module description',
            color=bot.colors["main"]
        )
        e.add_field(
            name=f"Commands [{len(cmds)}]",
            value="• "+f", ".join(f"`{cmd.qualified_name}`" for cmd in cmds)
        )
        if len(cmds) > 0:
            return await ctx.send(embed=e)
        await ctx.send(f'{bot.icons["warning"]} Module not found')

    async def send_group_help(self, group):
        ctx = self.context
        cmds = self.filter_commands(group.commands)
        e=discord.Embed(
            title=f"(G) {group.qualified_name} help".title(),
            description=group.help if group.help else 'No group description',
            color=bot.colors["main"]
        )
        e.add_field(
            name=f"Commands [{len(cmds)}]",
            value="• "+f", ".join(f"`{cmd.qualified_name}`" for cmd in cmds)
        )
        if len(cmds) > 0:
            return await ctx.send(embed=e)
        await ctx.send(f'{bot.icons["warning"]} Group not found')

    async def send_command_help(self, command : bot.get_command):
        ctx = self.context

        description = f"{command.description}" if command.description else "No command description"
        cmd_usage = f"{ctx.prefix}{command.qualified_name} {command.signature}".replace("_", " ") or f"{ctx.prefix}{command.qualified_name}"
        cmd_aliases = ", ".join(f"`{alias}`" for alias in command.aliases) or "No aliases"
        cmd_cooldown = f"`{humanize.precisedelta(command._buckets._cooldown.per)}`" if command._buckets._cooldown else "No cooldown"
        
        embed = discord.Embed(
            title=f"{command.qualified_name} command".title(),
            description=f"""
**Description:** {description}
**Cooldown:** {cmd_cooldown}
**Usage:** {cmd_usage}
**Aliases:** {cmd_aliases}
            """,
            colour=bot.colors["main"]
        )
        await ctx.send(embed=embed)

    async def send_error_message(self, error):
        ctx = self.context
        ctx.message.content = ctx.message.content.replace(ctx.prefix+"jsk dbg ","")
        command = ctx.message.content.lower().replace(ctx.prefix+"help ","")
        cog_ = []
        for cog in command.split():
            if bot.get_cog(cog):
                cog_.append(cog)
        if cog_:
            if len(cog_) > 3:
                return await ctx.send(f'{bot.icons["warning"]} You cannot request more than **3** categories at once')
            else:
                for cog in cog_:
                    await ctx.send_help(cog)
                    await asyncio.sleep(1)
        if not cog_:
            e=discord.Embed(
                title=f"{bot.user.name} help".title(),
                description=f"**<> = Required** | **[] = Required**",
                color=bot.colors["main"]
            )
            for cog in bot.cogs:
                cog = bot.get_cog(cog)
                cmds = await self.filter_commands(cog.get_commands())
                if len(cmds) > 0:
                    e.add_field(
                        name=f"{cog.qualified_name}".title(),
                        value="> "+", ".join(f'`{cmd.qualified_name}`' for cmd in cmds),
                        inline=False
                    )
            await ctx.send(embed=e)

bot.help_command = Help()

# run the bot

bot.run(token)