from .base_reacts import BaseReacts
from .emotions import Emotions
from .interactions import Interactions
from .fun import Fun

async def setup(bot):
    await bot.add_cog(BaseReacts(bot))
    await bot.add_cog(Emotions(bot))
    await bot.add_cog(Interactions(bot))
    await bot.add_cog(Fun(bot))
