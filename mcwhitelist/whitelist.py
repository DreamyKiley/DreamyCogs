from redbot.core import commands
import discord

class Whitelist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.allowed_guilds = {
            1111111111111111111: "Role1",     # Server1 -> Allowed role: "Role1"
            2222222222222222222: "Role2",        # Server2 -> Allowed role: "Role2"
            3333333333333333333: "Role3"          # Server3 -> Allowed role: "Role3"
        }
        self.channel_id = 1147253430113554433  # Target channel
        self.command_enabled = True  # Default state
        self.admin_users = {11111111111111111111, 22222222222222222, 33333333333333333}  # Allowed User-IDs

    @commands.command()
    async def mcadd(self, ctx, username: str):
        if not self.command_enabled:
            return await ctx.send("❌ The whitelist command is currently disabled.")

        guild_id = ctx.guild.id
        if guild_id not in self.allowed_guilds:
            return await ctx.send("This command can only be used in specific servers.")

        required_role_name = self.allowed_guilds[guild_id]
        user_roles = [role.name for role in ctx.author.roles]

        if required_role_name not in user_roles:
            return await ctx.send(f"❌ You need the `{required_role_name}` role to use this command.")

        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            return await ctx.send("I couldn't find the whitelist channel!")

        try:
            await channel.send(f"whitelist add {username}")
            await ctx.send(f"✅ Added `{username}` to the whitelist!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to send messages in the whitelist channel.")

    @commands.command()
    async def mcdisable(self, ctx):
        if ctx.author.id not in self.admin_users:
            return await ctx.send("❌ You do not have permission to use this command.")

        self.command_enabled = False
        await ctx.send("⚠️ The whitelist command has been **disabled**.")

    @commands.command()
    async def mcenable(self, ctx):
        if ctx.author.id not in self.admin_users:
            return await ctx.send("❌ You do not have permission to use this command.")

        self.command_enabled = True
        await ctx.send("✅ The whitelist command has been **enabled**.")

async def setup(bot):
    await bot.add_cog(Whitelist(bot))
