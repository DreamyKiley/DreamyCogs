# Hurray for templates from my other files <33

from redbot.core import commands
from discord import Embed
import random

class Fun(commands.Cog):
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

    @commands.command(name="explode")
    async def send_explode_image(self, ctx):
        await self._send_image(ctx, "explode-images", "{nickname} exploded, call the fire department!", 0xFF4500)

    @commands.command(name="headdesk")
    async def send_headdesk_image(self, ctx):
        await self._send_image(ctx, "headdesk-images", "*{nickname} headdesks* .. ouch", 0xC0C0C0)

    @commands.command(name="hide")
    async def send_hide_image(self, ctx):
        await self._send_image(ctx, "hide-images", "{nickname} hides", 0x2F4F40)

    @commands.command(name="lurk")
    async def send_lurk_image(self, ctx):
        await self._send_image(ctx, "lurk-images", "{nickname} is lurking", 0x4B0080)

    @commands.command(name="nosebleed")
    async def send_nosebleed_image(self, ctx):
        await self._send_image(ctx, "nosebleed-images", "{nickname} has a nose bleed, oh no!", 0xFF0000)

    @commands.command(name="sleep")
    async def send_sleep_image(self, ctx):
        await self._send_image(ctx, "sleep-images", "{nickname} is sleepy", 0x7B68FF)

    @commands.command(name="pout")
    async def send_pout_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} pouts at {target_nickname}" if user and user != ctx.author else "{nickname} is pouting, HMPH"
        await self._send_image(ctx, "pout-images", title, 0xFF69B0, user)

    @commands.command(name="blush")
    async def send_blush_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} blushes at {target_nickname}" if user and user != ctx.author else "{nickname} is blushing >//<"
        await self._send_image(ctx, "blush-images", title, 0xFFC0C0, user)

    @commands.command(name="shrug")
    async def send_shrug_image(self, ctx):
        await self._send_image(ctx, "shrug-images", "*{nickname} shrugs*", 0xB0C4D0)

    @commands.command(name="stare")
    async def send_stare_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} stares at {target_nickname} intently" if user and user != ctx.author else "{nickname} is staring"
        await self._send_image(ctx, "stare-images", title, 0x4682B4, user)

    @commands.command(name="yuck")
    async def send_yuck_image(self, ctx):
        await self._send_image(ctx, "yuck-images", "*{nickname} is grossed out*", 0x6A5ACD)

    @commands.command(name="flop")
    async def send_flop_image(self, ctx):
        await self._send_image(ctx, "flop-images", "*{nickname} flops over*", 0xF28C28)
