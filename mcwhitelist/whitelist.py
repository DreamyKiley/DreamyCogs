from redbot.core import commands
import discord

class Whitelist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.allowed_guilds = {
            11111111111111111111: "Role1",     # Server1 -> Allowed role: "Role1"
            22222222222222222222: "Scions",       # Server2 -> Allowed role: "Role2"
            33333333333333333333: "Gaming"         # Server3 -> Allowed role: "Role3"
        }
        self.channel_id = 44444444444444444  # Target channel, pairs with EssentialX Discord

    @commands.command()
    async def mcadd(self, ctx, username: str):
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

async def setup(bot):
    await bot.add_cog(Whitelist(bot))
