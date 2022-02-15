from pydoc import describe
from tkinter.messagebox import NO
from typing import Union
import discord
from discord.ext import commands
import asyncio
from discord.utils import get
from funcs import count
from main import bot as b
from data import warns

color = 0x2f3136

def can_execute_action(ctx: commands.Context, target: discord.Member):
    if ctx.author.id in b.owner_ids or \
        ctx.author.id == ctx.guild.owner.id or \
        ctx.author.top_role.position > target.top_role.position:
        return True
    else:
        return None

class moderation(commands.Cog):
    """Moderation commands to help keep your server together"""

    def __init__(self, bot):
        self.bot = b

    @commands.command(name="ban",description="bans a member",help="!ban @Shobi posting nsfw")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ban(self, ctx: commands.Context, member : discord.Member, *, reason = None):
        reason = reason or "No reason provided"

        if can_execute_action(ctx, member):
            try:
                await member.ban(reason=f"Action by {ctx.author} ({ctx.author.id}): {reason}")
                n=discord.Embed(
                    description=f"{self.bot.icons['check']} **{member} ({member.id})** was banned by {ctx.author.mention} for: **{reason}**",
                    color=self.bot.colors["main"]
                )
                await ctx.reply(embed=n,mention_author=False)
                try:
                    e=discord.Embed(
                        description=f"You were banned from **{ctx.guild.name}** for: **{reason}**",
                        color=self.bot.colors["main"]
                    )
                    await member.send(embed=e)
                except:
                    return
            except:
                a=discord.Embed(
                    description=f"{self.bot.icons['cross']} I do not have permission to ban this member",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(embed=a,mention_author=False)
        elif not can_execute_action(ctx, member):
            e=discord.Embed(
                description=f"{self.bot.icons['cross']} You do not have permission to ban this member",
                color=self.bot.colors["red"]
            )
            await ctx.reply(embed=e,mention_author=False)
    
    @commands.command(name="unban",description="unbans a user",help="!unban @Shobi dms appeal")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unban(self, ctx: commands.Context, user : discord.User, *, reason = None):
        member = user
        reason = reason or "No reason provided"
        try:
            await ctx.guild.unban(user, reason=f"Action by {ctx.author} ({ctx.author.id}): {reason}")
            n=discord.Embed(
                description=f"{self.bot.icons['check']} **{member} ({member.id})** was unbanned by {ctx.author.mention} for: **{reason}**",
                color=self.bot.colors["main"]
            )
            await ctx.reply(embed=n,mention_author=False)
            try:
                e=discord.Embed(
                    description=f"You were unbanned from **{ctx.guild.name}** for: **{reason}**",
                    color=self.bot.colors["main"]
                )
                await member.send(embed=e)
            except:
                return
        except:
            a=discord.Embed(
                description=f"{self.bot.icons['cross']} User **{user}** not found",
                color=self.bot.colors["red"]
            )
            await ctx.reply(embed=a,mention_author=False)

    @commands.command(name="kick",description="kicks a member",help="!kick @Shobi soft spam")
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kick(self, ctx: commands.Context, member : discord.Member, *, reason = None):
        if reason == None:
            reason = "No reason provided"
        if can_execute_action(ctx,member):
            try:
                await member.kick(reason=f"Action by {ctx.author} ({ctx.author.id}): {reason}")
                n=discord.Embed(
                    description=f"{self.bot.icons['check']} **{member} ({member.id})** was kicked by {ctx.author.mention} for: **{reason}**",
                    color=self.bot.colors["main"]
                )
                await ctx.reply(embed=n,mention_author=False)
                try:
                    e=discord.Embed(
                        description=f"You were kicked from **{ctx.guild.name}** for: **{reason}**",
                        color=self.bot.colors["main"]
                    )
                    await member.send(embed=e)
                except:
                    return
            except:
                a=discord.Embed(
                    description=f"{self.bot.icons['cross']} I do not have permission to kick this member",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(embed=a,mention_author=False)
        elif not can_execute_action(ctx,member):
            e=discord.Embed(
                description=f"{self.bot.icons['cross']} You do not have permission to kick this member",
                color=self.bot.colors["red"]
            )
            await ctx.reply(embed=e,mention_author=False)

    @commands.command(name="mute",description="Mutes a user for a certian reason",help="!mute @Shobi spam")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def mute(self, ctx: commands.Context, member : discord.Member, *, reason = None):
        # if reason is none
        reason = "no reason provided" if not reason else reason

        # gets the role

        muted_roles = []
        for role in ctx.guild.roles:
            if "muted" in role.name.lower():
                muted_roles.append(role.id)

        if muted_roles:
            if count(muted_roles) > 1:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"{self.bot.icons['warning']} You have {count(muted_roles)} roles with \"muted\" in the role name",
                        color=self.bot.colors["error"]
                    ),mention_author=False
                )
            else:
                role = discord.utils.get(ctx.guild.roles,id=muted_roles[0])
        else:
            e=discord.Embed(
                description=f'{self.bot.icons["cross"]} You need a role named "muted" for me to mute this member',
                color=self.bot.colors["red"]
            )
            return await ctx.reply(embed=e,mention_author=False)
            
        role_ = discord.utils.get(member.roles,name="Muted")
        if role_:
            e=discord.Embed(
                description=f"{self.bot.icons['cross']} This member is already muted",
                color=self.bot.colors["red"]
            )
            return await ctx.reply(embed=e,mention_author=False)

        # if the ctx.author does not have perms

        if not can_execute_action:
            e=discord.Embed(
                description=f"{self.bot.icons['cross']} You do not have permission to mute this member",
                color=self.bot.colors["red"]
            )
            return await ctx.reply(embed=e,mention_author=False)
        # else if the ctx.author DOES have the perms
        elif can_execute_action and not role_:
            # if the bot has perms
            try:
                await member.add_roles(role)
                e=discord.Embed(
                    description=f"{self.bot.icons['check']} **{member} ({member.id})** was muted by {ctx.author.mention} for: **{reason}**",
                    color=self.bot.colors["main"]
                )
                await ctx.reply(embed=e,mention_author=False)
                # if the bot can dm the member
                try:
                    a=discord.Embed(
                        description=f"You were muted in {ctx.guild.name} for: {reason}",
                        color=self.bot.colors["red"]
                    )
                    await member.send(embed=a)
                # if the bot cant dm the member
                except:
                    return
            # if the bot doesnt have perms
            except:
                n=discord.Embed(
                    description=f"{self.bot.icons['cross']} I do not have permission to mute this member",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(embed=n,mention_author=False)

    @commands.command(name="unmute",description="Unmutes a user")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unmute(self, ctx: commands.Context, member : discord.Member):
        
        muted_roles = []
        for role in member.roles:
            if "muted" in role.name.lower():
                muted_roles.append(role.id)
        if muted_roles:
            if count(muted_roles) > 1:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"{self.bot.icons['warning']} This member has {count(muted_roles)} muted roles",
                        color=self.bot.colors["red"]
                    ),mention_author=False
                )
            else:
                role = discord.utils.get(member.roles,id=muted_roles[0])
        else:
            e=discord.Embed(
                description=f'{self.bot.icons["warning"]} This member is not muted',
                color=self.bot.colors["red"]
            )
            return await ctx.reply(embed=e,mention_author=False)

        # if the ctx.author does not have perms

        if not can_execute_action(ctx,member):
            e=discord.Embed(
                description=f"{self.bot.icons['cross']} You do not have permission to unmute this member",
                color=self.bot.colors["red"]
            )
            await ctx.reply(embed=e,mention_author=False)
        # else if the ctx.author DOES have the perms
        elif can_execute_action(ctx,member) and role:
            # if the bot has perms
            try:
                await member.remove_roles(role)
                e=discord.Embed(
                    description=f"{self.bot.icons['check']} **{member} ({member.id})** was unmuted by {ctx.author.mention}",
                    color=self.bot.colors["main"]
                )
                await ctx.reply(embed=e,mention_author=False)
                # if the bot can dm the member
                try:
                    a=discord.Embed(
                        description=f"You were unmuted in **{ctx.guild.name}**",
                        color=self.bot.colors["main"]
                    )
                    await member.send(embed=a)
                # if the bot cant dm the member
                except:
                    return
            # if the bot doesnt have perms
            except:
                n=discord.Embed(
                    description=f"{self.bot.icons['cross']} I do not have permission to unmute this member",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(embed=n,mention_author=False)
    
    @commands.command(name="warn",description="warns a member",help="!warn @Shobi incorrect channel use")
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def warn(self, ctx: commands.Context, member : discord.Member, *, reason = None):
        if reason == None:
            reason = "No reason provided"
        
        if can_execute_action(ctx,member):
            n=discord.Embed(
                description=f'{self.bot.icons["check"]} **{member} ({member.id})** was warned by {ctx.author.mention} for: **{reason}**',
                color=self.bot.colors["main"]
            )
            if not warns.get(member.id):
                warns[member.id] = {ctx.guild.id: {1: reason}}

            elif warns.get(member.id):
                if not warns.get(member.id)[ctx.guild.id]:
                    warns[member.id][ctx.guild.id] = {1: reason}

                elif warns.get(member.id)[ctx.guild.id]:
                    warn_count = len(warns[member.id][ctx.guild.id]) + 1
                    warns[member.id][ctx.guild.id][warn_count] = reason

            await ctx.reply(embed=n,mention_author=False)
            try:
                e=discord.Embed(
                    description=f"You were warned in **{ctx.guild.name}** for: **{reason}**",
                    color=self.bot.colors["main"]
                )
                await member.send(embed=e)
            except:
                return
        elif not can_execute_action(ctx,member):
            e=discord.Embed(
                description=f"{self.bot.icons['cross']} You do not have permission to warn this member",
                color=self.bot.colors["red"]
            )
            await ctx.reply(embed=e,mention_author=False)
    
    @commands.command(description="Removes a warn from a member")
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def delwarn(self, ctx: commands.Context, member: discord.Member, warning_id: int):
        try:
            warns.get(member.id)[ctx.guild.id]
            warns[member.id][ctx.guild.id].pop(warning_id)
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['check']} Warning has been removed from **{member}**",
                    color=self.bot.colors["main"]
                ),mention_author=False
            )
        except:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} Either this user has no warnings or this ID is not found",
                    color=self.bot.colors["red"]
                ),mention_author=False
            )
    
    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def warnings(self, ctx: commands.Context, member: discord.Member):
        try:
            warnings = []
            for num, warn in warns[member.id][ctx.guild.id].items():
                warnings.append(f"{num}. {warn}")
            if warnings:
                return await ctx.reply(
                    embed=discord.Embed(
                        title=f"{member} warns",
                        description="\n".join(warnings),
                        color=self.bot.colors["main"]
                    ),mention_author=False
                )
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} **{member}** currently has no warns",
                    color=self.bot.colors["red"]
                ),mention_author=False
            )
        except:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} **{member}** currently has no warns",
                    color=self.bot.colors["red"]
                ),mention_author=False
            )

    @commands.command(description="Gives someone a nickname for the server")
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def nick(self, ctx: commands.Context, member : discord.Member, *, nickname = None):
        nickname = '' if not nickname else nickname
        if can_execute_action(ctx,member):
            try:
                await member.edit(nick=nickname)
                e=discord.Embed(
                    description=f"{self.bot.icons['check']} **{member.name}**'s nickname has been changed by {ctx.author.mention} to: `{nickname}`",
                    color=self.bot.colors["main"]
                )
                await ctx.reply(embed=e,mention_author=False)
                try:
                    n=discord.Embed(
                        description=f"Your nickname in **{ctx.guild.name}** has been changed to: `{nickname}`",
                        color=self.bot.colors["main"]
                    )
                    await member.send(embed=n)
                except:
                    return
            except:
                e=discord.Embed(
                    description=f"{self.bot.icons['cross']} I do not have permission to change this member's nickname",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(embed=e,mention_author=False)
        elif not can_execute_action(ctx,member):
            a=discord.Embed(
                description=f"{self.bot.icons['cross']} You do not have permission to change this member's nickname",
                color=self.bot.colors["red"]
            )
            await ctx.reply(embed=a,mention_author=False)
    
    @commands.command(description="Gives a role to the member")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def addrole(self, ctx: commands.Context, member : discord.Member, *, role : discord.Role):
        role = get(ctx.guild.roles, id=role.id)
        if can_execute_action(ctx,member):
            try:
                await member.add_roles(role)
                e=discord.Embed(
                    description=f"{self.bot.icons['check']} {role.mention} has been given by {ctx.author.mention} to {member} ({member.id})",
                    color=self.bot.colors["main"]
                )
                await ctx.reply(embed=e,mention_author=False)
                try:
                    a=discord.Embed(
                        description=f"You have been given the role of {role.mention} in: {ctx.guild.name}",
                        color=self.bot.colors["main"]
                    )
                    await member.send(embed=a)
                except:
                    return
            except:
                e=discord.Embed(
                    description=f"{self.bot.icons['cross']} I do not have permission to give that role to {member}",
                    color=self.bot.colors["red"]
                )
                await ctx.send(embed=e)
        elif not can_execute_action(ctx,member):
            a=discord.Embed(
                description=f"{self.bot.icons['cross']} You do not have permission to give that role to {member}",
                color=self.bot.colors["red"]
            )
            await ctx.reply(embed=a,mention_author=False)
    
    @commands.command(description="Removes a role from a member")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def removerole(self, ctx: commands.Context, member : discord.Member, *, role : discord.Role):
        role = get(ctx.guild.roles, id=role.id)
        if can_execute_action(ctx,member):
            try:
                await member.remove_roles(role)
                e=discord.Embed(
                    description=f"{self.bot.icons['check']} {member} ({member.id}) has been removed from {role.mention} by {ctx.author.mention}",
                    color=self.bot.colors["main"]
                )
                await ctx.reply(embed=e,mention_author=False)
                try:
                    a=discord.Embed(
                        description=f"Your role {role.mention} has been removed from you in: {ctx.guild.name}",
                        color=self.bot.colors["main"]
                    )
                    await member.send(embed=a)
                except:
                    return
            except:
                e=discord.Embed(
                    description=f"{self.bot.icons['cross']} I do not have permission to remove that role from {member}",
                    color=self.bot.colors["red"]
                )
                await ctx.reply(embed=e,mention_author=False)
        elif not can_execute_action(ctx,member):
            a=discord.Embed(
                description=f"{self.bot.icons['cross']} You do not have permission to remove that role from {member}",
                color=self.bot.colors["red"]
            )
            await ctx.reply(embed=a,mention_author=False)

    @commands.command(description="Purges a limited amount")
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: Union[int, str] = None):
        amount = 1 if amount is None else amount
        if isinstance(amount, str):
            if amount.lower() == "all":
                amount: int = 400
            else:
                return await ctx.reply(
                    embed=discord.Embed(
                        title=f"{self.bot.icons['warning']} | Invalid Argument",
                        description="Your amount must either be \"all\" or an integer!",
                        color=self.bot.colors["error"]
                    ),mention_author=False
                )
        if amount > 400 or amount < 1:
            return await ctx.reply(
                embed=discord.Embed(
                    title=f"{self.bot.icons['warning']} | Invalid Number",
                    description="Your number must be either 400 or below: not including a negative or 0",
                    color=self.bot.colors["error"]
                ),mention_author=False
            )
        
        data = {}
        await ctx.message.delete()
        msgs = await ctx.channel.purge(limit=amount)
        for msg in msgs:
            msg: discord.Message = msg
            try:data[msg.author.id]+=1
            except:data[msg.author.id]=1
        Data = {}
        for id, n in data.items():
            Data[f"**{self.bot.get_user(id).name}#{self.bot.get_user(id).discriminator}**"] = n
        m = await ctx.send(
            embed=discord.Embed(
                title=f"{len(msgs)} Messages Purged",
                description="\n".join(f"{author}: {num}" for author, num in Data.items()),
                color=self.bot.colors["main"]
            )
        )
        await asyncio.sleep(3)
        return await m.delete()
    
    @commands.command(description="edits a channel to be invisible for everyone apart from administrators and the owner")
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invisible(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        try:
            await channel.edit(
                overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
                }
            )

            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['check']} Made {channel.mention} invisible",
                    color=self.bot.colors["main"]
                ),mention_author=False
            )
        except:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} I don't have access to edit this channel",
                    color=self.bot.colors["red"]
                ),mention_author=False
            )
    
    @commands.command(description="edits a channel to be visible for everyone")
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def visible(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        try:
            await channel.edit(
                overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=True)
                }
            )

            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['check']} Made {channel.mention} visible",
                    color=self.bot.colors["main"]
                ),mention_author=False
            )
        except:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"{self.bot.icons['warning']} I don't have access to edit this channel",
                    color=self.bot.colors["red"]
                ),mention_author=False
            )

    @commands.command(name="slowmode",aliases=["channelslowmode","slowmodechannel"],description="edits a channel's slowmode",help="!slowmode 5 #general")
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slowmode(self, ctx: commands.Context, seconds : float, channel : discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        if seconds > 21600:
            e=discord.Embed(
                description=f"{self.bot.icons['cross']} The slowmode's maximum is 6 hours (21600 seconds)",
                color=self.bot.colors["red"]
            )
            await ctx.reply(
                embed=e,
                mention_author=False
            )
        else:
            await channel.edit(slowmode_delay=seconds)
            e=discord.Embed(
                description=f"{self.bot.icons['check']} I have set {channel.mention}'s slowmode to {seconds} seconds",
                color=self.bot.colors["main"]
            )
            await ctx.reply(
                embed=e,
                mention_author=False
            )
    
def setup(bot):
    bot.add_cog(moderation(bot))