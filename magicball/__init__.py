from .magic_eight_ball import MagicEightBall

async def setup(bot):
    await bot.add_cog(MagicEightBall(bot))
