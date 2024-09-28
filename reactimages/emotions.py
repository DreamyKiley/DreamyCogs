# Hurray for google and thanks to a friend helping push me to refactor to clean stuff a lot, also correction, would be a helper class if I understood properly

from redbot.core import commands
from discord import Embed
import random

class Emotions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_reacts = None

    async def cog_load(self):
        from .base_reacts import BaseReacts
        cog = self.bot.get_cog("BaseReacts")
        if cog:
            self.base_reacts = cog

    async def _check_category(self, ctx, category: str):
        if category not in self.base_reacts.image_dict or not self.base_reacts.image_dict[category]:
            await ctx.send(f"No images found for category: {category}")
            return False
        return True

    async def _send_image(self, ctx, category: str, title: str, color: int, user: commands.MemberConverter = None):
        if not await self._check_category(ctx, category):
            return
        
        image_url = random.choice(self.base_reacts.image_dict[category])
        nickname = ctx.author.display_name
        if user:
            target_nickname = user.display_name
            title = title.format(nickname=nickname, target_nickname=target_nickname)
        else:
            title = title.format(nickname=nickname)
        
        embed = Embed(color=color)
        embed.set_image(url=image_url)
        embed.set_author(name=title, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="happy")
    async def send_happy_image(self, ctx):
        await self._send_image(ctx, "happy-images", "{nickname} is so happy! :>", 0xFFFF00)

    @commands.command(name="amazed")
    async def send_amazed_image(self, ctx):
        await self._send_image(ctx, "amazed-images", "{nickname} is amazed! WOAH!", 0x00CFFF)

    @commands.command(name="angry")
    async def send_angry_image(self, ctx):
        await self._send_image(ctx, "angry-images", "{nickname} is angry! grrr", 0xFF4C4C)

    @commands.command(name="confused")
    async def send_confused_image(self, ctx):
        await self._send_image(ctx, "confused-images", "{nickname} is a little confused", 0xF7C63C)

    @commands.command(name="sad")
    async def send_sad_image(self, ctx):
        await self._send_image(ctx, "sad-images", "{nickname} is sad", 0x6C8EBF)

    @commands.command(name="cry")
    async def send_cry_image(self, ctx):
        await self._send_image(ctx, "cry-images", "{nickname} is crying :<", 0xA5C5E8)

    @commands.command(name="smug")
    async def send_smug_image(self, ctx):
        await self._send_image(ctx, "smug-images", "{nickname} is really smug", 0xDB6E6E)

    @commands.command(name="scared")
    async def send_scared_image(self, ctx):
        await self._send_image(ctx, "scared-images", "{nickname} is scared!", 0xFA6161)

    @commands.command(name="lonely")
    async def send_lonely_image(self, ctx):
        await self._send_image(ctx, "lonely-images", "{nickname} is lonely, give them a hug. </3", 0x8F9DB5)

    @commands.command(name="cute")
    async def send_cute_image(self, ctx):
        await self._send_image(ctx, "cute-images", "{nickname} is being so cute!", 0xFFB6C0)

    @commands.command(name="love")
    async def send_love_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} loves {target_nickname}, awww <3" if user and user != ctx.author else "You're deserving of love {nickname}, tell someone else you love them now!"
        await self._send_image(ctx, "love-images", title, 0xFF6F60, user)

    @commands.command(name="laugh")
    async def send_laugh_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} laughs at {target_nickname}" if user and user != ctx.author else "{nickname} laughs LOL"
        await self._send_image(ctx, "laugh-images", title, 0xFFB6C0, user)

    @commands.command(name="plead")
    async def send_plead_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} pleads with {target_nickname}" if user and user != ctx.author else "{nickname} pleads"
        await self._send_image(ctx, "plead-images", title, 0xA0A0FA, user)

    @commands.command(name="shocked")
    async def send_shocked_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} is shocked by {target_nickname}" if user and user != ctx.author else "{nickname} is shocked"
        await self._send_image(ctx, "shocked-images", title, 0xFAD614, user)

    @commands.command(name="annoyed")
    async def send_annoyed_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} is annoyed with {target_nickname}" if user and user != ctx.author else "{nickname} is annoyed"
        await self._send_image(ctx, "annoyed-images", title, 0xDB6E6E, user)
