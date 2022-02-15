import discord
from discord.ext import commands
import datetime
import time
from discord.ext import menus
from discord.ext.menus.views import ViewMenuPages
from numerize.numerize import numerize as n
from funcs import count, last
from main import bot as b


UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]

def pretty_size(bytes, units=UNITS_MAPPING):
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


color = 0x2f3136
actual = datetime.datetime.utcnow()
timee = actual.strftime("%a, %d %b %Y %I:%M %p")
avatar = "https://cdn.discordapp.com/attachments/381963689470984203/874600331256946758/ShiFun_Official_Icon.png"

class info(commands.Cog):
    """Information commands for information"""

    def __init__(self, bot):
        self.bot = b

    @commands.command(name="botinfo",aliases=["about","whoami"],description="info on the bot",help="!botinfo")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def botinfo(self, ctx):
        shobi = self.bot.get_user(self.bot.owner_ids[0])
        shibe = self.bot.get_user(self.bot.owner_ids[1])
        e=discord.Embed(
            description=f"Hello! I am {self.bot.user.name}. I am a bot dedicated to the purpose of keeping your server in health!",
            color=self.bot.colors["main"]
        )
        e.set_author(
            name=f"{self.bot.user.name} Info",
            icon_url=self.bot.user.avatar.url
        )
        e.add_field(
            name="General",
            value=f"""
**Developers:** `{shobi}`, `{shibe}`
**Name:** {self.bot.user.name}
**Avatar URL:** [click here]({self.bot.user.avatar.url})
            """,
            inline=False
        )
        e.add_field(
            name="Bot",
            value=f"""
**Guilds:** {len(self.bot.guilds)}
**Users:** {len(self.bot.users)}
**Commands:** {len([cmd for cmd in self.bot.commands if not cmd.hidden])}
            """,
            inline=False
        )
        await ctx.reply(
            embed=e,
            mention_author=False
        )

    @commands.command(name="userinfo", aliases=["ui", "memberinfo", "mi","whois"],description="gets info on someone",help="!userinfo @Shobi")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def userinfo(self, ctx, *, member : discord.Member = None):
        member = member or ctx.author

        # VARIABLES
        if member.top_role.name == "@everyone":
            top_role = "no top role".title()
            toprole_position = 0
        else:
            top_role = member.top_role.mention
            toprole_position = member.top_role.position

        if "offline" != str(member.mobile_status):
            platform = "Mobile"
        elif "offline" != str(member.desktop_status):
            platform = "Desktop"
        elif "offline" != str(member.web_status):
            platform = "Web"
        else:
            platform = "None"
        
        if member.guild_permissions.kick_members == True:
            mod = self.bot.icons["check"]
        elif member.guild_permissions.kick_members == False:
            mod = self.bot.icons["cross"]
        if member.guild_permissions.administrator == True:
            admin = self.bot.icons["check"]
        elif member.guild_permissions.administrator == False:
            admin = self.bot.icons["cross"]
        if member.bot:
            bot_ = self.bot.icons["check"]
        else:
            bot_ = self.bot.icons["cross"]
    
        # ----------------------------
    
        e=discord.Embed(
            description=f"""
**{self.bot.icons['arrow']} ID:** {member.id}
**{self.bot.icons['arrow']} Joined:** {discord.utils.format_dt(member.joined_at, "F")} ({discord.utils.format_dt(member.joined_at, "R")})
**{self.bot.icons['arrow']} Nick:** {member.nick}
**{self.bot.icons['arrow']} Platform:** {platform}
**{self.bot.icons['arrow']} Registered:** {discord.utils.format_dt(member.created_at, "F")} ({discord.utils.format_dt(member.created_at, "R")})
**{self.bot.icons['arrow']} Bot:** {bot_}

**{self.bot.icons['arrow']} Admin:** {admin}
**{self.bot.icons['arrow']} Moderator:** {mod}
**{self.bot.icons['arrow']} Roles [{len(member.roles) - 1}]:** {' '.join(role.mention for role in member.roles if not role.name == "@everyone"[:30]) or "No roles"}
**{self.bot.icons['arrow']} Top Role:** {top_role} ({toprole_position})

**{self.bot.icons['arrow']} Permissions:** {', '.join(f"`{perm}`".title().replace("_"," ") for perm, value in member.guild_permissions if value)}
            """,
            color=self.bot.colors["main"]
        )
        e.set_thumbnail(
            url=member.guild_avatar.url if member.guild_avatar else ''
        )
        e.set_author(
            name=member,
            icon_url=member.avatar.url if member.avatar else ''
        )
        await ctx.reply(
            embed=e,
            mention_author=False
        )

    @commands.command(name="serverinfo", aliases=["guildinfo", "gi", "si"],description="gets info on the server",help="!serverinfo")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def serverinfo(self, ctx : commands.Context):
        guild = ctx.guild
        humans = bots = total = online = dnd = idle = offline = staff = animated = static = 0
        for e in guild.emojis:
            if e.animated:
                animated += 1
            elif not e.animated:
                static += 1
        for m in guild.members:
            total += 1
            if m.guild_permissions.kick_members and not m.bot:
                staff += 1
            if not m.bot:
                humans += 1
            elif m.bot:
                bots += 1
            if m.raw_status == "online":
                online += 1
            elif m.raw_status == "dnd":
                dnd += 1
            elif m.raw_status == "idle":
                idle += 1
            elif m.raw_status == "offline":
                offline += 1

        if str(guild.explicit_content_filter) == "no_role":
            explictContentFilter = "Scan media content from members without a role".title()
            
        elif str(guild.explicit_content_filter) == "all_members":
            explictContentFilter = "Scan media from all members".title()
        else:
            explictContentFilter = "Don't scan any media content".title()

        e=discord.Embed(
            title=guild.name,
            description=guild.description if guild.description else 'No server description',
            color=self.bot.colors["main"]
        )
        e.set_thumbnail(
            url=guild.icon.url if guild.icon else ''
        )
        e.set_image(
            url=guild.banner.url if guild.banner else ''
        )
        e.add_field(
            name="Members",
            value=f"""
{self.bot.icons['arrow']} Owner: {guild.owner.mention}
{self.bot.icons['arrow']} Humans: {n(humans)}
{self.bot.icons['arrow']} Staff: {n(staff)}
{self.bot.icons['arrow']}*Bots: {n(bots)}
{self.bot.icons['arrow']} Total: {n(total)}
{self.bot.icons['arrow']} Limit: {n(guild.max_members)}
            """,
            inline=False
        )
        e.add_field(
            name=f"Statuses",
            value=f"""
{self.bot.icons['arrow']} Online: {n(online)}
{self.bot.icons['arrow']} DND: {n(dnd)}
{self.bot.icons['arrow']} Idle: {n(idle)}
{self.bot.icons['arrow']} Offline: {n(offline)}
            """,
            inline=False
        )
        e.add_field(
            name=f"Channels",
            value=f"""
{self.bot.icons['arrow']} Text: {count(guild.text_channels)} (+{count([i for i in guild.text_channels if i.nsfw])} NSFW)
{self.bot.icons['arrow']} Voice: {count(guild.voice_channels)}
{self.bot.icons['arrow']} Category: {count(guild.categories)}
{self.bot.icons['arrow']} Stages: {count(guild.stage_channels)}
{self.bot.icons['arrow']} Threads: {count(guild.threads)}
            """,
            inline=False
        )
        e.add_field(
            name=f"Emojis",
            value=f"""
{self.bot.icons['arrow']} Total: {n(count(guild.emojis))}/{n(guild.emoji_limit)}
{self.bot.icons['arrow']} Static: {n(static)}/{n(guild.emoji_limit)}
{self.bot.icons['arrow']} Animated: {n(animated)}/{n(guild.emoji_limit)}
            """,
            inline=False
        )
        e.add_field(
            name=f"Boosts",
            value=f"""
{self.bot.icons['arrow']} Level: {n(guild.premium_tier)}
{self.bot.icons['arrow']} Boosts: {n(guild.premium_subscription_count)}
{self.bot.icons['arrow']} Role: {guild.premium_subscriber_role.mention if guild.premium_subscriber_role else None}
{self.bot.icons['arrow']} Latest
            """,
            inline=False
        )
        e.add_field(
            name="Other",
            value=f"""
{self.bot.icons['arrow']} Verification Level: {str(guild.verification_level).title()}
{self.bot.icons['arrow']} NSFW Level: {explictContentFilter}
{self.bot.icons['arrow']} Filesize Limit: {pretty_size(guild.filesize_limit)}
{self.bot.icons['arrow']} Roles: {len(guild.roles)}
{self.bot.icons['arrow']} Created: {discord.utils.format_dt(guild.created_at, "F")} ({discord.utils.format_dt(guild.created_at, "R")})
{self.bot.icons['arrow']} Region: {guild.region}
            """,
            inline=False
        )
        await ctx.reply(
            embed=e,
            mention_author=False
        )
    
    @commands.command(name="guildchannels",description="see all the server channels",help="!guildchannels")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def guildchannels(self, ctx: commands.Context):
        guild = ctx.guild
        m = await ctx.send(f'{self.bot.icons["loading"]} Loading channels...')
        e=discord.Embed(
            title=f"{guild.name} channels",
            description="\n".join(f"**{i.name}**\n"+"\n".join(f"{'<:online:877563239859384350>'+c.mention if ctx.author in c.members else '<:offline:877563239486087178>'+c.mention}" for c in i.channels) for i in guild.categories),
            color=self.bot.colors["main"]
        )
        await ctx.send(embed=e)
        await m.delete()
    
    @commands.command(name="serverroles",aliases=["guildroles"],description="see all the server roles",help="!serveroles")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def serverroles(self, ctx: commands.Context):
        bot_ = self.bot
        ab = []
        for role in ctx.guild.roles:
            if role.name != "@everyone":
                ab.append(f"{role.mention}")
        class EmbedPageSource(menus.ListPageSource):
            async def format_page(self, menu, ab):
                embed = discord.Embed(
                    description=" ".join(ab) or "No roles",
                    color=bot_.colors["main"]
                )
                embed.set_author(
                    name=f"{ctx.guild.name} Roles [{len(ctx.guild.roles) - 1}]",
                    icon_url=ctx.guild.icon.url
                )
                return embed
        menu = ViewMenuPages(source=EmbedPageSource(ab, per_page=35))
        await ctx.send('Menu is below')
        await menu.start(ctx)
    
    @commands.command(name="userroles",aliases=["memberroles"],description="see all of someone's roles",help="!userroles @Shobi")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def memberroles(self, ctx: commands.Context, *, member : discord.Member = None):
        bot_ = self.bot
        if member == None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
        
        class EmbedPageSource2(menus.ListPageSource):
            async def format_page(self, menu, ab):
                embed = discord.Embed(
                    description="\n".join(ab) or "No roles",
                    color=bot_.colors["main"]
                )
                embed.set_author(
                    name=f"{member} Roles [{len(member.roles) - 1}]",
                    icon_url=member.avatar.url
                )
                return embed
        ab = []
        for role in member.roles:
            if role.name != "@everyone":
                ab.append(f"{role.mention}")
        menu = ViewMenuPages(source=EmbedPageSource2(ab, per_page=15))
        await ctx.send('Menu is below')
        await menu.start(ctx)
    
    @commands.command(name="roleusers",description="gets all the users that have a certian role",help="!roleusers @Members")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def roleusers(self, ctx: commands.Context, *, role : discord.Role):
        members = 0
        bot_ = self.bot
        class EmbedPageSource2(menus.ListPageSource):
            async def format_page(self, menu, roleusers):
                e=discord.Embed(
                    title=f"Role Members [{len(role.members)}]",
                    description="\n".join(roleusers) or "No members",
                    color=bot_.colors["main"]
                )
                return e
        roleusers = []
        for member in role.members:
            members+=1
            roleusers.append(f"`{members}.` **{member}** | `{member.id}` | {role.mention}")
        menu = ViewMenuPages(source=EmbedPageSource2(roleusers, per_page=15))
        await ctx.send('Menu is below')
        await menu.start(ctx)
    
    @commands.command(name="roleinfo",description="gets info on a certian role",help="!roleusers @Members")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def roleinfo(self, ctx: commands.Context, *, role : discord.Role):
        perms = []
        for permission, value in role.permissions:
            if value:
                perms.append(f"`{permission}`".replace("_", " ").title())
        e=discord.Embed(
            description=f"""
**Mention:** {role.mention}
**ID:** {role.id}
**Name:** {role.name}
**Colour:** {str(role.color)}
**Created:** {discord.utils.format_dt(role.created_at, "F")} ({discord.utils.format_dt(role.created_at, "R")})
**Postion:** {role.position}
**Members:** {len(role.members)}
**Permissions:** {", ".join(p for p in perms)}
            """,
            color=self.bot.colors["main"]
        )
        await ctx.reply(
            embed=e,
            mention_author=False
        )
    
    @commands.command(name="ping",description="get the bot's ping",help="!ping")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def ping(self, ctx):
        start = time.perf_counter()
        e=discord.Embed(
            description=f"{self.bot.icons['loading']} Loading latency...",
            color=self.bot.colors["main"]
        )
        msg = await ctx.reply(
            embed=e,
            mention_author=False
        )
        end = time.perf_counter()
        a=discord.Embed(
            title="🏓 Pong!",
            color=self.bot.colors["main"]
        )
        a.add_field(
            name=f"{self.bot.icons['loading']} | Latency",
            value=f"`{self.bot.latency:.3f}s`"
        )
        a.add_field(
            name=f"{self.bot.icons['typing']} | Typing",
            value=f"`{end - start:.3f}s`"
        )
        await msg.edit(embed=a)

    @commands.command(name="emoji",description="just a way of copying an emoji i guess",help="!emoji <:doge_bonk:892447832848601180>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def emoji(self, ctx, emoji : discord.PartialEmoji):
        e=discord.Embed(
            title=f"`:{emoji.name}:`",
            color=self.bot.colors["main"]
        )
        e.set_image(
            url=emoji.url
        )
        await ctx.reply(
            embed=e,
            mention_author=False
        )


    @commands.command(name="permissions", aliases=["perms", "permission", "perm"],description="see a user's permissions",help="!permissions @Shobi")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def permissions(self, ctx, *, member : discord.Member = None):
        bot_ = self.bot
        member = member or ctx.author
        ab = []
        for permission, value in member.guild_permissions:
            if value:
                ab.append(f"{self.bot.icons['check']} {permission}".replace("_", " ").title())
            elif not value:
                ab.append(f"{self.bot.icons['cross']} {permission}".replace("_", " ").title())
        class EmbedPageSource5(menus.ListPageSource):
            async def format_page(self, menu, ab):
                embed = discord.Embed(
                    title=f"{member} permissions",
                    description="\n".join(ab),
                    color=bot_.colors["main"]
                )
                return embed
        await ctx.send('Menu is below')
        menu = ViewMenuPages(source=EmbedPageSource5(ab, per_page=20))
        await menu.start(ctx)

def setup(bot):
    bot.add_cog(info(bot))