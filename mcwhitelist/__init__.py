from .whitelist import Whitelist

async def setup(bot):
    await bot.add_cog(Whitelist(bot))
