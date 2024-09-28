# Did this for a friends server I host on

import random
from redbot.core import commands
from discord import Embed

class MagicEightBall(commands.Cog):
    """Magic Eight Ball Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def magic_eight_ball(self, ctx, *, question: str = None):
        """Ask the magic eight ball a question."""
        if not question:
            await ctx.send("You need to ask a question, i.e., `!8ball will I win this roll?`")
            return

        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes – definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]

        response = random.choice(responses)
        
        embed = Embed(
            title="🎱 The Magic 8-Ball says...",
            description=(
                f"**Question:** {question}\n"
                f"**Answer:** {response}\n\n"
                f"[DreamyCogs](https://github.com/DreamyKiley/DreamyCogs/)\n\n"
            ),
            color=0x0A57c2  # Magic8ball Blue color
        )

        await ctx.send(embed=embed)

# Don't forget to add the cog to the bot
def setup(bot):
    bot.add_cog(MagicEightBall(bot))
