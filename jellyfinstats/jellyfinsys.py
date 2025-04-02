import aiohttp
import random
from discord import Embed
from redbot.core import commands, Config
import asyncio

ALLOWED_USERS = {111, 222, 333}  # Replace with actual Discord user IDs

class JellyfinWatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=156302847392649182)
        self.config.register_global(jellyfin_api_key="your_api_key_here", jellyfin_host="your_host_here")  # Optional: can be ignored with !jfapi

    async def get_currently_watching(self):
        api_key = await self.config.jellyfin_api_key()
        host = await self.config.jellyfin_host()
        url = f"http://{host}/Sessions"
        headers = {"X-Emby-Token": api_key}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return None
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            print(f"Error fetching Jellyfin data: {e}")
            return None

    def create_embed(self, username, media_type, device_name, title, description, color):
        """ Helper function to create the embed for each session. """
        return Embed(
            title=f"{username} {title}",
            description=f"{media_type} on **{device_name}**\n{description}",
            color=color
        )

    @commands.command(name="jfwatch")
    async def jellyfin_watch(self, ctx: commands.Context):
        if ctx.author.id not in ALLOWED_USERS:  # Check if user is in the ALLOWED_USERS list
            await ctx.send("You are not authorized to use this command.")
            return

        data = await self.get_currently_watching()

        if not data:
            await ctx.send("Couldn't retrieve data from Jellyfin. Please check the API settings.")
            return

        embeds = []
        for session in data:
            username = session.get("UserName", "Unknown User")
            now_playing_item = session.get("NowPlayingItem", {})
            device_name = session.get("DeviceName", "Unknown Device")

            if now_playing_item:
                media_type = now_playing_item.get("Type", "Unknown")
                is_transcoding = session.get("Transcoding", False)
                playback_status = "Direct Play" if not is_transcoding else "Transcoding"
                description = now_playing_item.get("Overview", "No description available.")

                if media_type == "Movie":
                    movie_title = now_playing_item.get("Name", "Unknown Movie")
                    description = f"**{movie_title}**\n{playback_status}\n\n{description}"
                    session_embed = self.create_embed(username, "🎬 Movie", device_name, "watching", description, 0x800080)  # Purple

                elif media_type == "Episode":
                    show_name = now_playing_item.get("SeriesName", "Unknown Show")
                    season = now_playing_item.get("SeasonName", "Unknown Season")
                    episode_number = now_playing_item.get("IndexNumber", "Unknown Episode Number")
                    formatted_season_episode = f"{season} / Episode {episode_number}"
                    description = f"**{show_name}**\n{formatted_season_episode}\n{playback_status}\n\n{description}"
                    session_embed = self.create_embed(username, "📺 TV Show", device_name, "watching", description, 0x0000FF)  # Blue

                elif media_type == "Audio":
                    track_name = now_playing_item.get("Name", "Unknown Track")
                    artist_name = now_playing_item.get("AlbumArtist", "Unknown Artist")
                    album_name = now_playing_item.get("Album", "Unknown Album")
                    description = f"**{track_name}** by **{artist_name}**\nAlbum: *{album_name}*\n{playback_status}\n\n{description}"
                    session_embed = self.create_embed(username, "🎵 Music", device_name, "listening to", description, 0x00FFFF)  # Cyan

                embeds.append(session_embed)

        if embeds:
            await ctx.send(embeds=embeds)
        else:
            await ctx.send("No one is currently watching or listening to anything.")

    @commands.command(name="jfallow")
    async def jfallow(self, ctx: commands.Context, user_id: int):
        """ Adds a user to the ALLOWED_USERS list (only accessible by the bot owner) """
        if ctx.author.id != self.bot.owner_id:
            await ctx.send("You do not have permission to add users.")
            return
        
        global ALLOWED_USERS
        if user_id not in ALLOWED_USERS:
            ALLOWED_USERS.add(user_id)  # Add the user ID to the ALLOWED_USERS set
            await ctx.send(f"User {user_id} has been added to the allowed list.")
        else:
            await ctx.send(f"User {user_id} is already on the allowed list.")

    @commands.command(name="jfapi")  # Can be skipped if manually set on line 11
    async def set_jellyfin_api(self, ctx: commands.Context, api_key: str):
        await self.config.jellyfin_api_key.set(api_key)
        await ctx.send("Jellyfin API key has been updated successfully. Now, please enter the host URL and port (e.g., 123.456.789:1000).")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await ctx.bot.wait_for("message", check=check, timeout=60)
            await self.config.jellyfin_host.set(msg.content.strip())
            await ctx.send("Jellyfin host has been updated successfully.")
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Please try setting the host again with the correct format.")
