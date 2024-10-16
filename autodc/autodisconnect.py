# Will write readme and everything else later
import discord
import asyncio
from redbot.core import commands

class AutoDisconnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and before.channel != after.channel:
            await self.check_empty_channel(before.channel)

    async def check_empty_channel(self, channel):
        voice_client = discord.utils.get(self.bot.voice_clients, channel=channel)
        if voice_client and len(channel.members) == 1 and channel.members[0] == self.bot.user:
            await asyncio.sleep(5)
            if len(channel.members) == 1 and channel.members[0] == self.bot.user:
                await voice_client.disconnect()
