from .weather import WeatherCog

async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
