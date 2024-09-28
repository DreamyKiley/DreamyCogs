from .cmdcleaner import CmdCleaner

async def setup(bot):
    await bot.add_cog(CmdCleaner(bot))
