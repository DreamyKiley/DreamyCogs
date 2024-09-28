from redbot.core import commands, Config
from discord import Embed
import time
import asyncio

class Levels(commands.Cog):

    LEVEL_CAP = 100
    MAX_PRESTIGE = 10
    XP_PER_MESSAGE = 10
    LEVEL_UP_BASE_XP = 100
    XP_SCALING_FACTOR = 1.15

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=759480213645791683)
        self.config.register_guild(levels={}, last_message={}, leveling_enabled=True, delete_after=None)
        self.config.register_member(level_up_notifications=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild, author = message.guild, message.author
        if not await self.config.guild(guild).leveling_enabled():
            return

        current_time = time.time()
        user_id = str(author.id)
        guild_data, last_message = await self.config.guild(guild).levels(), await self.config.guild(guild).last_message()

        user_data = guild_data.get(user_id, {"level": 0, "xp": 0, "prestige": 0})
        if current_time - last_message.get(user_id, 0) >= 10:
            user_data["xp"] += self.XP_PER_MESSAGE
            await self.process_level_up(message, author, guild_data, user_data)
            last_message[user_id] = current_time

            await self.config.guild(guild).levels.set(guild_data)
            await self.config.guild(guild).last_message.set(last_message)

    async def process_level_up(self, message, author, guild_data, user_data):
        while user_data["xp"] >= self.calculate_xp_for_next_level(user_data["level"]):
            if user_data["level"] >= self.LEVEL_CAP:
                user_data["xp"] = self.calculate_xp_for_next_level(user_data["level"])
                break

            user_data["level"] += 1
            user_data["xp"] -= self.calculate_xp_for_next_level(user_data["level"])

            if user_data["level"] >= 25 and user_data["prestige"] < self.MAX_PRESTIGE:
                user_data.update({"level": 1, "xp": 0, "prestige": user_data["prestige"] + 1})
                await message.channel.send(f"Congratulations {author.mention}! You've prestiged to **Prestige {user_data['prestige']}** and are now at Level 1!")

            if await self.config.member(author).level_up_notifications():
                msg = await message.channel.send(f"Congratulations {author.mention}! You've leveled up to **Level {user_data['level']}**!")
                delete_after = await self.config.guild(message.guild).delete_after()
                if delete_after:
                    await asyncio.sleep(delete_after)
                    await self.safe_delete(msg)

    def calculate_xp_for_next_level(self, level):
        return self.LEVEL_UP_BASE_XP * (self.XP_SCALING_FACTOR ** level)

    async def safe_delete(self, message):
        try:
            await message.delete()
        except discord.errors.NotFound:
            pass

    @commands.command(name="level")
    async def check_level(self, ctx, user: commands.MemberConverter = None):
        user = user or ctx.author
        guild_data = await self.config.guild(ctx.guild).levels()
        user_data = guild_data.get(str(user.id), {"level": 0, "xp": 0, "prestige": 0})

        embed = Embed(
            title=f"{user.display_name}'s Level",
            description=f"**Level:** {user_data.get('level', 0)} (Prestige: {user_data.get('prestige', 0)})\n**XP:** {round(user_data.get('xp', 0))}",
            color=0x00FF00
        )
        xp_needed = self.calculate_xp_for_next_level(user_data["level"]) - user_data["xp"]
        embed.set_footer(text=f"Required XP: {round(xp_needed)} - Messages: {round(xp_needed / self.XP_PER_MESSAGE)}")

        await ctx.send(embed=embed)

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx, page: int = 1):
        """Display the leveling leaderboard for the server with pagination."""
        guild_data = await self.config.guild(ctx.guild).levels()

        # Ensure all user data has the 'prestige' key and purge users who left
        to_remove = []
        for user_id in list(guild_data):
            user = ctx.guild.get_member(int(user_id))
            if user is None:
                to_remove.append(user_id)  # Mark users who left for removal

        # Remove the users who left from guild_data
        for user_id in to_remove:
            del guild_data[user_id]

        # Save the updated guild data back to the config
        await self.config.guild(ctx.guild).levels.set(guild_data)

        # Sort users by prestige, level, and XP, setting default values if any key is missing
        sorted_users = sorted(guild_data.items(), key=lambda item: (
            item[1].get("prestige", 0),  # Default prestige is 0 if missing
            item[1].get("level", 0),     # Default level is 0 if missing
            item[1].get("xp", 0)         # Default xp is 0 if missing
        ), reverse=True)

        if not sorted_users:
            await ctx.send("No users found in the leaderboard.")
            return

        items_per_page = 10
        max_pages = (len(sorted_users) + items_per_page - 1) // items_per_page
        page = max(1, min(page, max_pages))

        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        leaderboard_text = ""
        for index, (user_id, data) in enumerate(sorted_users[start_index:end_index], start=start_index + 1):
            user = ctx.guild.get_member(int(user_id))
            if user:
                leaderboard_text += f"{index}. {user.display_name} - Level {data.get('level', 0)} (Prestige {data.get('prestige', 0)})\n"

        embed = Embed(
            title=f"Leaderboard for {ctx.guild.name}\n(Page {page}/{max_pages})",
            description=leaderboard_text or "No data available for this page.",
            color=0x00FF00
        )
        embed.set_footer(text="Powered by DreamyCogs")

        message = await ctx.send(embed=embed)

        if page > 1:
            await message.add_reaction("⬅️")
        if page < max_pages:
            await message.add_reaction("➡️")

        def check(reaction, user):
            return user != self.bot.user and reaction.message.id == message.id and reaction.emoji in ["⬅️", "➡️"]

        try:
            while True:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                if reaction.emoji == "⬅️" and page > 1:
                    await message.delete()
                    await self.leaderboard(ctx, page - 1)
                    break
                elif reaction.emoji == "➡️" and page < max_pages:
                    await message.delete()
                    await self.leaderboard(ctx, page + 1)
                    break
        except asyncio.TimeoutError:
            pass

    @commands.command(name="togglelevels")
    @commands.admin()
    async def toggle_levels(self, ctx):
        current_status = await self.config.guild(ctx.guild).leveling_enabled()
        new_status = not current_status
        await self.config.guild(ctx.guild).leveling_enabled.set(new_status)
        status_text = "enabled" if new_status else "disabled"
        await ctx.send(f"Leveling system has been {status_text}.")

    @commands.command(name="setlevel")
    @commands.admin()
    async def set_level(self, ctx, user: commands.MemberConverter, level: int):
        """Manually sets a user's level."""
        if level < 0 or level > self.LEVEL_CAP:
            await ctx.send(f"Please provide a level between 0 and {self.LEVEL_CAP}.")
            return

        guild_data = await self.config.guild(ctx.guild).levels()
        user_data = guild_data.get(str(user.id), {"level": 0, "xp": 0, "prestige": 0})
    
        # Update user data
        user_data["level"] = level
        user_data["xp"] = 0  # Reset XP upon level change
        guild_data[str(user.id)] = user_data

        # Save updated guild data
        await self.config.guild(ctx.guild).levels.set(guild_data)
    
        # Send confirmation message
        await ctx.send(f"{user.display_name}'s level has been set to **Level {level}**!")

    @commands.command(name="setxp")
    @commands.admin()
    async def set_xp(self, ctx, user: commands.MemberConverter, xp: int):
        """Manually sets a user's XP."""
        if xp < 0:
            await ctx.send("XP cannot be negative.")
            return

        guild_data = await self.config.guild(ctx.guild).levels()
        user_data = guild_data.get(str(user.id), {"level": 0, "xp": 0, "prestige": 0})
        user_data["xp"] = xp
        guild_data[str(user.id)] = user_data

        await self.config.guild(ctx.guild).levels.set(guild_data)
        await ctx.send(f"{user.display_name}'s XP has been set to **{xp}**!")

    @commands.command(name="resetlevel")
    @commands.admin()
    async def reset_level(self, ctx, user: commands.MemberConverter):
        """Resets a user's level and XP."""
        guild_data = await self.config.guild(ctx.guild).levels()
        if str(user.id) in guild_data:
            del guild_data[str(user.id)]

        await self.config.guild(ctx.guild).levels.set(guild_data)
        await ctx.send(f"{user.display_name}'s level and XP have been reset.")

    @commands.command(name="levelmsg")
    async def toggle_level_up_notifications(self, ctx):
        """Toggles level-up notifications for the user."""
        current_setting = await self.config.member(ctx.author).level_up_notifications()
        await self.config.member(ctx.author).level_up_notifications.set(not current_setting)
        new_status = "enabled" if not current_setting else "disabled"
        await ctx.send(f"Level-up notifications have been {new_status}.")

    @commands.command(name="levelmsgdel")
    @commands.admin()
    async def set_delete_after(self, ctx, seconds: int):
        """Sets the number of seconds after which level-up messages are deleted."""
        if seconds < 0:
            await ctx.send("Seconds cannot be negative.")
            return

        await self.config.guild(ctx.guild).delete_after.set(seconds)
        if seconds == 0:
            await ctx.send("Messages will not be deleted after level-up.")
        else:
            await ctx.send(f"Level-up messages will be deleted after {seconds} seconds.")

    @commands.command(name="setprestige")
    @commands.admin()
    async def set_prestige(self, ctx, user: commands.MemberConverter, prestige: int):
        """Manually sets a user's prestige."""
        if prestige < 0 or prestige > self.MAX_PRESTIGE:
            await ctx.send(f"Please provide a prestige between 0 and {self.MAX_PRESTIGE}.")
            return

        guild_data = await self.config.guild(ctx.guild).levels()
        user_data = guild_data.get(str(user.id), {"level": 0, "xp": 0, "prestige": 0})
        user_data["prestige"] = prestige
        user_data["level"] = 1  # Reset level to 1 upon prestige change
        guild_data[str(user.id)] = user_data

        await self.config.guild(ctx.guild).levels.set(guild_data)
        await ctx.send(f"{user.display_name}'s prestige has been set to **Prestige {prestige}**!")
