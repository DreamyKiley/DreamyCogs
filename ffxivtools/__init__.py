from .ffxivtools import FFXIVTools

async def setup(bot):
    await bot.add_cog(FFXIVTools(bot))
