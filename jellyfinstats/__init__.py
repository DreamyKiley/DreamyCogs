from .jellyfinsys import JellyfinWatch

async def setup(bot):
    await bot.add_cog(JellyfinWatch(bot))
