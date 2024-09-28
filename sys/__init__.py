from .botstats import BotStats

async def setup(bot):
    await bot.add_cog(BotStats(bot))
