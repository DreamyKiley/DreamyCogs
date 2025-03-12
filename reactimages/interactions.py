from redbot.core import commands
from discord import Embed
import random

class Interactions(commands.Cog):
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

    @commands.command(name="hug")   # Template prevents no user mentioned
    async def send_hug_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to hug.")
    
        title = "{nickname} is hugging {target_nickname}" if user != ctx.author else "It's okay {nickname}, I'll hug you.. but try hugging someone else!"
        await self._send_image(ctx, "hug-images", title, 0xFFB6C0, user)

    @commands.command(name="cuddle")
    async def send_cuddle_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to cuddle.")
    
        title = "{nickname} cuddles with {target_nickname} <3" if user != ctx.author else "We can cuddle {nickname}, but try cuddling someone else!"
        await self._send_image(ctx, "cuddle-images", title, 0xFFDAB0, user)

    @commands.command(name="kiss")
    async def send_kiss_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to kiss.")
    
        title = "{nickname} kisses {target_nickname}" if user != ctx.author else "What are you kissing {nickname}? A mirror?"
        await self._send_image(ctx, "kiss-images", title, 0xFF69B5, user)

    @commands.command(name="clap")  # Template handles self if "!clap @self" and "!clap"
    async def send_clap_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} claps for {target_nickname}" if user and user != ctx.author else "{nickname} is clapping"
        await self._send_image(ctx, "clap-images", title, 0xF4A460, user)

    @commands.command(name="poke")
    async def send_poke_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to poke.")
    
        title = "{nickname} pokes {target_nickname}" if user != ctx.author else "{nickname}.. Why are you poking yourself weirdo?"
        await self._send_image(ctx, "poke-images", title, 0xC0C0C0, user)

    @commands.command(name="slap")  # Template prevents image if self mentioned
    async def send_slap_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to slap.")
    
        if user == ctx.author:
            nickname = ctx.author.display_name
            return await ctx.send(f"{nickname} Please don't slap yourself! D: Get help.")
    
        title = "{nickname} slaps {target_nickname}"
        await self._send_image(ctx, "slap-images", title, 0xFF6550, user)

    @commands.command(name="punch")
    async def send_punch_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to punch.")
    
        if user == ctx.author:
            nickname = ctx.author.display_name
            return await ctx.send(f"{nickname} you dummy! Don't punch yourself! Punch others, embrace chaos!")
    
        title = "{nickname} punches {target_nickname}"
        await self._send_image(ctx, "punch-images", title, 0xE0E0E0, user)

    @commands.command(name="pat")
    async def send_pat_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to pat.")
    
        title = "{nickname} pats {target_nickname}" if user != ctx.author else "Don't worry {nickname}, I got you! *headpats you* :>\nYou're doing a great job today!"
        await self._send_image(ctx, "pat-images", title, 0xEDEDED, user)

    @commands.command(name="lick")
    async def send_lick_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} licks {target_nickname}" if user and user != ctx.author else "{nickname} is licking at random, watch out!"
        await self._send_image(ctx, "lick-images", title, 0xF6C1C1, user)

    @commands.command(name="spank")
    async def send_spank_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to.. spank..")
    
        title = "{nickname} spanks {target_nickname}" if user != ctx.author else "I mean if you really want {nickname}, not my place to judge."
        await self._send_image(ctx, "spank-images", title, 0xFF4500, user)

    @commands.command(name="wave")
    async def send_wave_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} waves at {target_nickname}" if user and user != ctx.author else "{nickname} is waving at random people"
        await self._send_image(ctx, "wave-images", title, 0x87CEEB, user)

    @commands.command(name="dance")
    async def send_dance_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} dances with {target_nickname}" if user and user != ctx.author else "{nickname} is dancing"
        await self._send_image(ctx, "dance-images", title, 0xFF1490, user)

    @commands.command(name="bite", aliases=["nom"])
    async def send_vite_image(self, ctx, user: commands.MemberConverter = None):
        title = "{nickname} bites {target_nickname}, NOM!" if user and user != ctx.author else "{nickname} bites at random, so spooky!"
        await self._send_image(ctx, "bite-images", title, 0x8F2424, user)

    @commands.command(name="kill")
    async def send_kill_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("I don't condone this, but please mention a user to kill.")
    
        if user == ctx.author:
            return await ctx.send(f"Why are you like this?")
    
        title = "{nickname} kills {target_nickname}"
        await self._send_image(ctx, "kill-images", title, 0x8C1C1C, user)

    @commands.command(name="highfive")
    async def send_highfive_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to highfive.")
    
        title = "{nickname} highfives {target_nickname}, nice!" if user != ctx.author else "*highfives {nickname}* You're not alone :D"
        await self._send_image(ctx, "highfive-images", title, 0x09FF0, user)

    @commands.command(name="bonk")
    async def send_bonk_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to bonk.")
    
        title = "*{nickname} bonks {target_nickname}* D:<" if user != ctx.author else "*bonks {nickname}* .. D-did you just bonk yourself?"
        await self._send_image(ctx, "bonk-images", title, 0xFF4500, user)

    @commands.command(name="tackle")
    async def send_bonk_image(self, ctx, user: commands.MemberConverter = None):
        if not user:
            return await ctx.send("Please mention a user to tackle.")
    
        title = "*{nickname} tackles {target_nickname}*" if user != ctx.author else "You can't tackle yourself.. {nickname}, you can try and I can watch though"
        await self._send_image(ctx, "tackle-images", title, 0xFF4500, user)
