import asyncio
import aiohttp
import math
import statistics
import re
from discord import Embed
from redbot.core import commands
from xivlodestone import LodestoneScraper
from bs4 import BeautifulSoup

class FFXIVTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scraper = LodestoneScraper()

    @commands.command(name="char")
    async def lookup_character(self, ctx, *, name: str):
        async with ctx.channel.typing():
            try:
                results = [char async for char in self.scraper.search_characters(name, limit=10)]
                if not results:
                    return await ctx.send(f"No characters found for **{name}** on the Lodestone.")
                chosen = results[0] if len(results) == 1 else await self._choose_char(ctx, results)
                if not chosen:
                    return
                full_char = await self.scraper.get_character(chosen.id)
                await self.send_character_embed(ctx, full_char)
            except Exception as e:
                await ctx.send(f"Error fetching character data:\n{e}")

    async def _choose_char(self, ctx, options):
        menu = "Multiple characters found:\n"
        emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        options = options[:10]
        for idx, char in enumerate(options):
            menu += f"{emojis[idx]} **{char.name}** on **{char.world}**\n"
        msg = await ctx.send(menu)
        for i in range(len(options)):
            await msg.add_reaction(emojis[i])

        def check(r, u):
            return u == ctx.author and r.message.id == msg.id and str(r.emoji) in emojis[:len(options)]

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            idx = emojis.index(str(reaction.emoji))
            await msg.delete()
            return options[idx]
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send("Timed out, Please try again.")
            return None

    async def send_character_embed(self, ctx, char):
        lodestone_url = f"https://na.finalfantasyxiv.com/lodestone/character/{char.id}/"
        embed = Embed(title=char.name, url=lodestone_url, color=0x3498db)
        async with aiohttp.ClientSession() as session:
            async with session.get(lodestone_url) as resp:
                html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")

        icon_tag = soup.select_one("div.character__class_icon img")
        job_icon_url = icon_tag["src"] if icon_tag else None
        portrait_img = soup.select_one("div.character__detail__image a.js__image_popup img")
        portrait_url = portrait_img["src"] if portrait_img else None

        slots_map = {
            "mainhand": 0,
            "offhand": 1,
            "head": 2,
            "body": 3,
            "hands": 4,
            "legs": 6,
            "feet": 7,
            "earring": 8,
            "necklace": 9,
            "bracelet": 10,
            "ring1": 11,
            "ring2": 12,
        }

        ilvls = {}
        for slot, idx in slots_map.items():
            gear_div = soup.select_one(f".icon-c--{idx}")
            if not gear_div:
                continue
            tooltip_div = gear_div.find("div", class_="db-tooltip__item__level")
            if tooltip_div and tooltip_div.text.strip():
                match = re.search(r"\d+", tooltip_div.text)
                if match:
                    ilvls[slot] = int(match.group())
                else:
                    ilvls[slot] = 0
            else:
                ilvls[slot] = 0

        mainhand_ilvl = ilvls.get("mainhand", 0)
        if ilvls.get("offhand", 0) == 0:
            ilvls["offhand"] = mainhand_ilvl

        average_slots = [
            "mainhand", "offhand", "head", "body", "hands", "legs", "feet",
            "earring", "necklace", "bracelet", "ring1", "ring2"
        ]

        used_ilvls = [ilvls[slot] for slot in average_slots if ilvls.get(slot, 0) > 0]

        if used_ilvls:
            total_ilvl = sum(used_ilvls)
            count = len(used_ilvls)
            average_ilvl = total_ilvl // count
            item_level = str(average_ilvl)
        else:
            item_level = "Unknown"

        if job_icon_url:
            embed.set_thumbnail(url=job_icon_url)
        elif portrait_url:
            embed.set_thumbnail(url=portrait_url)
        if portrait_url:
            embed.set_image(url=portrait_url)

        def safe_get(attr):
            val = getattr(char, attr, None)
            return val if val else "Unknown"

        fc = getattr(char, "free_company", None)
        fc_name = getattr(fc, "name", fc) if fc else "None"

        embed.add_field(name="Server", value=safe_get("world"), inline=True)
        embed.add_field(name="FC", value=fc_name, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Level", value=str(safe_get("level")), inline=True)
        embed.add_field(name="iLvl", value=item_level, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)

        await ctx.send(embed=embed)
