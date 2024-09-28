from .pepe import PepeCog

async def setup(bot):
    await bot.add_cog(PepeCog(bot))
