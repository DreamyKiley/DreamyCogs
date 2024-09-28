from .message_logger import MessageLogger

async def setup(bot):
    await bot.add_cog(MessageLogger(bot))
