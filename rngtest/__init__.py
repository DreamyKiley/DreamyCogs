from .luckbot import LuckBot

async def setup(bot):
    await bot.add_cog(LuckBot(bot))
