import random
from redbot.core import commands
from discord import Embed

class LuckBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll")
    async def roll_number(self, ctx, number: int = None):
        """Roll a random number between 1 and the specified maximum (up to 100)."""
        if not number or number <= 0:
            await ctx.send("Please provide a valid positive integer, e.g., `!roll 100`.")
            return

        if number > 100:
            await ctx.send("The maximum number allowed is 100. Please provide a number between 1 and 100.")
            return

        result = random.randint(1, number)
        user = ctx.author.display_name  # Get the user's display name
        
        embed = Embed(
            title="🎲 Roll Result",
            description=(
                f"**{user}** rolling out of {number}\n\n"
                f"**{result}**\n\n"
                f"[DreamyCogs](https://github.com/DreamyKiley/DreamyCogs/)\n\n"
            ),
            color=0xAFA176  # old mmorpg color <3
        )

        await ctx.send(embed=embed)

    @commands.command(name="flip")
    async def flip_coin(self, ctx):
        """Flip a coin to get either Heads or Tails."""
        result = random.choice(["Heads", "Tails"])
        user = ctx.author.display_name  # Get the user's display name

        embed = Embed(
            title="🪙 Coin Flip",
            description=(
                f"**{user}** flipped a coin\n\n"
                f"**{result}**!\n\n"
                f"[DreamyCogs](https://github.com/DreamyKiley/DreamyCogs/)\n\n"
            ),
            color=0xAFA176  # old mmorpg color <3
        )

        await ctx.send(embed=embed)

# Don't forget to add the cog to the bot
def setup(bot):
    bot.add_cog(LuckBot(bot))
