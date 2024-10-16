# Will write readme and everything else later
from .autodisconnect import AutoDisconnect

async def setup(bot):
    await bot.add_cog(AutoDisconnect(bot))
