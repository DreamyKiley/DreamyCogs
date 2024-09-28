# __init__.py
from .level import Levels

async def setup(bot):
    await bot.add_cog(Levels(bot))
