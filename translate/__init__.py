from .disctranslator import DiscTranslator

async def setup(bot):
    await bot.add_cog(DiscTranslator(bot))
