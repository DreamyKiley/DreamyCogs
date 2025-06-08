import asyncio
import aiohttp
import re
from discord import Embed
from redbot.core import commands
from xivlodestone import LodestoneScraper
from bs4 import BeautifulSoup

# Future: Fix item level parsing that makes me angy
# -- Job Stones/Materia do not affect/Round to the nearest lower number, 13 slots for PAL/WHM/BLM - 12 for other --
# Dirty way to just grab char data with LodestoneScraper, and scraping HTML to grab the item level

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

        # Extract job icon/portrait
        icon_tag = soup.select_one("div.character__class_icon img")
        job_icon_url = icon_tag["src"] if icon_tag else None
        portrait_img = soup.select_one("div.character__detail__image a.js__image_popup img")
        portrait_url = portrait_img["src"] if portrait_img else None

        # I'm lazy and don't know how FFXIV calculates Item Levels so I just have it grabbing the highest for equipped gear.
        # Other methods I *did* try was parsing the number from <div class="character__detail__avg">, but this is just as jank as they're not publicly visible it appears.
        # It only took me 2 hours to figure that out when using my own char as the test dummy :)
        item_levels = []
        highest_ilvl = 0
        highest_slot = "Unknown"

        for i in range(2, 14):  # icon-c--2 to icon-c--13
            gear_div = soup.select_one(f".icon-c--{i}")
            if not gear_div:
                continue
            tooltip = gear_div.find_next("div", class_="db-tooltip__item__level")
            if tooltip:
                match = re.search(r"\d+", tooltip.text)
                if match:
                    ilvl = int(match.group())
                    item_levels.append(ilvl)
                    if ilvl > highest_ilvl:
                        highest_ilvl = ilvl
                        slot_name_tag = gear_div.find_next("div", class_="db-tooltip__item__category")
                        highest_slot = slot_name_tag.text.strip() if slot_name_tag else f"Slot {i}"

        if item_levels:
            item_level = f"{highest_ilvl}"
        else:
            item_level_div = soup.select_one("div.character__detail__avg")
            item_level = item_level_div.text.strip() if item_level_div else "Unknown"
           # I'm tired and going to sleep. :)

        # Image
        if job_icon_url:
            embed.set_thumbnail(url=job_icon_url)
        elif portrait_url:
            embed.set_thumbnail(url=portrait_url)
        if portrait_url:
            embed.set_image(url=portrait_url)

        # character
        def safe_get(attr):
            val = getattr(char, attr, None)
            return val if val else "Unknown"

        fc = getattr(char, "free_company", None)
        fc_name = getattr(fc, "name", fc) if fc else "None"

        # Fuck these finnicky ass discord embeds
        embed.add_field(name="Server", value=safe_get("world"), inline=True)
        embed.add_field(name="FC", value=fc_name, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)  # Spacer
        embed.add_field(name="Level", value=str(safe_get("level")), inline=True)
        embed.add_field(name="iLvl", value=item_level, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)  # Spacer
       # embed.add_field(name="Race", value=safe_get("race"), inline=True) ALL HAIL THE BNUUY RACE

        await ctx.send(embed=embed)
