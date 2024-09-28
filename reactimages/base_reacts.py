from redbot.core import commands, Config
from discord import Embed
import random
import re
from pathlib import Path

class BaseReacts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=92464250575879474)
        default_global = {"image_dict": {}, "image_filepath": ""}
        self.config.register_global(**default_global)
        self.image_dict = {}

    async def cog_load(self):
        """Called when the cog is loaded."""
        await self.load_image_list()

    async def cog_reload(self):
        """Reload image list on cog reload."""
        await self.load_image_list()

    async def load_image_list(self):
        """Load image list from the file path stored in config."""
        filepath = await self.config.image_filepath()
        if isinstance(filepath, str) and filepath:
            path = Path(filepath)
            if path.is_file():
                self.image_dict = self._parse_image_file(filepath)
            else:
                print(f"File not found at {filepath}. Please check the path.")
        else:
            print("No valid file path configured. Use the `!imagelist` command to set it.")

    @commands.command(name="imagelist")
    @commands.is_owner()
    async def load_images_list(self, ctx, filepath: str):
        """Load images from a specified text file and save the file path."""
        path = Path(filepath)
        if not path.is_file():
            await ctx.send("File not found. Please check the path and try again.")
            return

        self.image_dict = self._parse_image_file(filepath)
        await self.config.image_dict.set(self.image_dict)
        await self.config.image_filepath.set(filepath)
        await ctx.send("Image list loaded and saved successfully!")

    @commands.command(name="imagereload")
    @commands.is_owner()
    async def reload_image_list(self, ctx):
        """Reload the image list from the file path stored in config."""
        await self.load_image_list()
        await ctx.send("Image list reloaded successfully!")

    def _parse_image_file(self, filepath: str):
        """Parse the imagelist.txt file and return a dictionary."""
        image_dict = {}
        with open(filepath, 'r') as f:
            content = f.read()
            categories = re.findall(r"(\w+-images)\s*{([^}]*)}", content, re.MULTILINE | re.DOTALL)
            for category, urls in categories:
                url_list = re.findall(r"https?://[^\s]+", urls)
                url_list = [self._convert_dropbox_url(url) for url in url_list]
                image_dict[category.lower()] = url_list
        return image_dict

    def _convert_dropbox_url(self, url: str) -> str:
        """Convert Dropbox URL to direct download link."""
        if 'dropbox.com' in url:
            if '?dl=' in url:
                url = url.replace('?dl=0', '?raw=1')
            else:
                url += '?raw=1'
        return url

    async def _send_image(self, ctx, category: str, action: str):
        """Send a random image from a specified category."""
        if not self.image_dict:
            self.image_dict = await self.config.image_dict()
            if not self.image_dict:
                await ctx.send("No images found. Please load an image list first using the `!imagelist` command.")
                return
            
        category = category.lower()
        if category not in self.image_dict or not self.image_dict[category]:
            await ctx.send(f"No images found for category: {category}")
            return

        image_url = random.choice(self.image_dict[category])
        
        nickname = ctx.author.display_name
        embed = Embed(
            title=f"{nickname} is {action}",
            color=0xFF69B4
        )
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
