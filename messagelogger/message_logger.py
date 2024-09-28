# Make the Message Edited a little prettier, add timestamps of when a message was edited, add a join.leave

from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import escape
from discord import Embed, TextChannel

class MessageLogger(commands.Cog):
    """Message Logger Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=194827364590283746)
        self.config.register_guild(log_channel=None, excluded_channels=[], excluded_roles=[], excluded_users=[])

    @commands.command(name="logchannel")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel: TextChannel):
        """Sets the channel where message logs will be sent for the specific server."""
        await self.config.guild(ctx.guild).log_channel.set(channel.id)
        await ctx.send(f"Log channel set to {channel.mention} for this server.")

    @commands.command(name="log")
    @commands.has_permissions(administrator=True)
    async def log_toggle(self, ctx, *items):
        """Toggles inclusion or exclusion of specific channels, roles, or users from message logging."""
        guild_config = self.config.guild(ctx.guild)
        channels = set()
        roles = set()
        users = set()

        for item in items:
            if item.startswith("<#") and item.endswith(">"):
                channel_id = int(item.strip("<>#"))
                channels.add(channel_id)
            elif item.startswith("<@&") and item.endswith(">"):
                role_id = int(item.strip("<@&>"))
                roles.add(role_id)
            elif item.startswith("<@") and item.endswith(">"):
                user_id = int(item.strip("<@>"))
                users.add(user_id)
            else:
                try:
                    if item.startswith("#"):
                        item = item.strip("#")
                        channel = await commands.TextChannelConverter().convert(ctx, f"#{item}")
                        channels.add(channel.id)
                    elif item.startswith("@"):
                        item = item.strip("@")
                        role = await commands.RoleConverter().convert(ctx, f"@{item}")
                        roles.add(role.id)
                    else:
                        user = await commands.UserConverter().convert(ctx, item)
                        users.add(user.id)
                except Exception as e:
                    await ctx.send(f"Error converting '{item}' to a channel, role, or user: {e}")
                    return

        if channels:
            excluded_channels = set(await guild_config.excluded_channels())
            if channels.issubset(excluded_channels):
                excluded_channels.difference_update(channels)
                action_message = "re-included in"
            else:
                excluded_channels.update(channels)
                action_message = "excluded from"
            await guild_config.excluded_channels.set(list(excluded_channels))
            excluded_channel_mentions = ', '.join(f"<#{channel_id}>" for channel_id in channels if self.bot.get_channel(channel_id))
            await ctx.send(f"Channels {action_message} logging: {excluded_channel_mentions}")

        if roles:
            excluded_roles = set(await guild_config.excluded_roles())
            if roles.issubset(excluded_roles):
                excluded_roles.difference_update(roles)
                action_message = "re-included in"
            else:
                excluded_roles.update(roles)
                action_message = "excluded from"
            await guild_config.excluded_roles.set(list(excluded_roles))
            excluded_role_mentions = ', '.join(f"<@&{role_id}>" for role_id in roles if ctx.guild.get_role(role_id))
            await ctx.send(f"Roles {action_message} logging: {excluded_role_mentions}")

        if users:
            excluded_users = set(await guild_config.excluded_users())
            if users.issubset(excluded_users):
                excluded_users.difference_update(users)
                action_message = "re-included in"
            else:
                excluded_users.update(users)
                action_message = "excluded from"
            await guild_config.excluded_users.set(list(excluded_users))
            excluded_user_mentions = ', '.join(f"<@{user_id}>" for user_id in users if self.bot.get_user(user_id))
            await ctx.send(f"Users {action_message} logging: {excluded_user_mentions}")

    @commands.command(name="loghelp")
    async def log_help(self, ctx):
        """Provides information on how to use the logging."""
        help_message = (
            "**Message Logger Help**\n\n"
            "1. **Set the log channel:** `!logchannel #channel`\n"
            "   - Sets the channel where message logs will be sent.\n\n"
            "2. **Toggle channels, roles, or users for logging:** `!log #channel1 #channel2 ...` or `!log @role1 @role2 ...` or `!log @username1 @username2 ...`\n"
            "   - Excludes or includes specific channels, roles, or users in message logging.\n\n"
            "For more information, visit [Created by Kiley W.](https://github.com/DreamyKiley)"
        )
        await ctx.send(help_message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:  # Skip if the message author is a bot
            return

        guild_config = self.config.guild(message.guild)
        log_channel_id = await guild_config.log_channel()
        if not log_channel_id:
            return
        log_channel = self.bot.get_channel(log_channel_id)
        if not log_channel:
            return

        excluded_channels = set(await guild_config.excluded_channels())
        excluded_users = set(await guild_config.excluded_users())
        excluded_roles = set(await guild_config.excluded_roles())

        if message.channel.id in excluded_channels or message.author.id in excluded_users:
            return
        if any(role.id in excluded_roles for role in message.author.roles):
            return

        author_username = message.author.name
        author_id = message.author.id
        author_avatar_url = message.author.display_avatar.url

        embed = Embed(
            title=f"Message Deleted in {message.channel.mention}",
            description=f"{author_username} (ID: `{author_id}`)\n\n**Content:**\n```{escape(message.content)}```",
            color=0xFF0000  # Red color for delete messages
        )
        embed.set_thumbnail(url=author_avatar_url)  # Set the avatar as a thumbnail
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:  # Skip if the message author is a bot
            return

        guild_config = self.config.guild(before.guild)
        log_channel_id = await guild_config.log_channel()
        if not log_channel_id:
            return
        log_channel = self.bot.get_channel(log_channel_id)
        if not log_channel:
            return

        excluded_channels = set(await guild_config.excluded_channels())
        excluded_users = set(await guild_config.excluded_users())
        excluded_roles = set(await guild_config.excluded_roles())

        if before.channel.id in excluded_channels or before.author.id in excluded_users:
            return
        if any(role.id in excluded_roles for role in before.author.roles):
            return

        if before.content != after.content:
            author_username = before.author.name
            author_id = before.author.id
            author_avatar_url = before.author.display_avatar.url

            message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"

            embed = Embed(
                title=f"Message Edited in {before.channel.mention}",
                description=(    # Removed codeblock because it annoyed me, if you want to revert it check below comments
                    f"{author_username} (ID: `{author_id}`)\n\n"
                    f"**Before:**\n{escape(before.content)}\n\n"    # ```\n{escape(before.content)}\n```
                    f"**After:**\n{escape(after.content)}\n\n"    # ```\n{escape(before.content)}\n
                    f"[Jump to Message]({message_link})"
                ),
                color=0x00FF00  # Green color for edited messages
            )
            embed.set_thumbnail(url=author_avatar_url)  # Set the avatar as a thumbnail
            await log_channel.send(embed=embed)
