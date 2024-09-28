from redbot.core import commands, checks
from redbot.core.config import Config
import asyncio

class CmdCleaner(commands.Cog):

    predefined_commands = {"sys", "sys2"}

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=928214250575879474)
        self.config.register_guild(blocked_commands=[])

    @commands.Cog.listener()
    async def on_message(self, message):
        """Automatically delete specific commands after 1 second."""
        if message.author == self.bot.user:
            return  # Ignore messages from the bot itself

        # Fetch the list of blocked commands from the configuration
        blocked_commands = await self.config.guild(message.guild).blocked_commands()
        
        # Add predefined commands to the list of blocked commands
        all_blocked_commands = set(blocked_commands).union(self.predefined_commands)

        # Check if the message starts with any of the blocked commands
        if any(message.content.startswith(f"!{cmd}") for cmd in all_blocked_commands):
            await asyncio.sleep(1)  # Change this to make it wait in seconds before deleting the messages
            try:
                await message.delete()  # Delete the command message
            except Exception as e:
                print(f"Failed to delete message: {e}")

    def is_server_owner_or_bot_owner():
        async def predicate(ctx):
            # Check if the user is either the server owner or the bot owner
            return ctx.author.id == ctx.guild.owner_id or await ctx.bot.is_owner(ctx.author)
        return commands.check(predicate)

    @commands.guild_only()
    @is_server_owner_or_bot_owner()
    @commands.command(name="cmdc")
    async def cmd_cleaner(self, ctx, *commands_to_block):
        """Block or unblock commands in the current server."""
        blocked_commands = await self.config.guild(ctx.guild).blocked_commands()
        blocked_list = []
        unblocked_list = []

        if not commands_to_block:
            await ctx.send("You need to specify commands to block/unblock.")
            return

        for cmd in commands_to_block:
            cmd = cmd.lower()
            if cmd.startswith("!"):
                cmd = cmd[1:]  # Remove leading "!"
            if cmd in blocked_commands:
                blocked_commands.remove(cmd)
                unblocked_list.append(f"!{cmd}")
            else:
                blocked_commands.append(cmd)
                blocked_list.append(f"!{cmd}")

        # Save the updated list of blocked commands
        await self.config.guild(ctx.guild).blocked_commands.set(blocked_commands)

        # Format and send all collected messages in a single response
        blocked_message = "Blocked command(s): " + " ".join(blocked_list) if blocked_list else ""
        unblocked_message = "Unblocked command(s): " + " ".join(unblocked_list) if unblocked_list else ""
        response = "\n".join(msg for msg in [blocked_message, unblocked_message] if msg)

        if response:
            await ctx.send(f"```\n{response}\n```")

    @commands.guild_only()
    @is_server_owner_or_bot_owner()
    @commands.command(name="cmdcdelall")
    async def cmd_cleaner_delete_all(self, ctx):
        """Remove all blocked commands from the config excluding predefined ones."""
        blocked_commands = await self.config.guild(ctx.guild).blocked_commands()
        # Remove all commands that are not predefined
        filtered_commands = [cmd for cmd in blocked_commands if cmd not in self.predefined_commands]
        await self.config.guild(ctx.guild).blocked_commands.set(list(self.predefined_commands))  # Set only predefined commands

        if filtered_commands:
            await ctx.send(f"Removed commands: {', '.join(f'!{cmd}' for cmd in filtered_commands)}")
        else:
            await ctx.send("No commands were removed.")

    @commands.guild_only()
    @is_server_owner_or_bot_owner()
    @commands.command(name="cmdclist")
    async def cmd_cleaner_list(self, ctx):
        """List all blocked commands."""
        blocked_commands = await self.config.guild(ctx.guild).blocked_commands()
        # Exclude predefined commands
        current_blocked_commands = [cmd for cmd in blocked_commands if cmd not in self.predefined_commands]
        
        if current_blocked_commands:
            commands_list = ', '.join(f"!{cmd}" for cmd in current_blocked_commands)
            await ctx.send(f"Blocked commands: {commands_list}")
        else:
            await ctx.send("No commands are currently blocked.")

def setup(bot):
    bot.add_cog(CmdCleaner(bot))
