import aiohttp
from redbot.core import commands
import random
import os

class PepeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pepo")    # Friend told me to make the command pepo?
    @commands.cooldown(1, 5, commands.BucketType.user)  # Set a cooldown of 1 use per 5s per user
    async def get_pepe(self, ctx):
        
        file_path = os.path.join(os.path.dirname(__file__), "pepe.txt") 
        
        try:
            with open(file_path, "r") as file:
                pepe_images = file.readlines()

            pepe_images = [url.strip() for url in pepe_images if url.strip()]  # Remove any empty lines
            
            # Choose a random image
            selected_image = random.choice(pepe_images)

            # Fix the URL before making the request
            selected_image = selected_image.replace(
                "https://archive.org/download/", "https://ia804501.us.archive.org/3/items/"
            )

            # Use SSL=False to ignore SSL certificate verification errors
            async with aiohttp.ClientSession() as session:
                async with session.get(selected_image, allow_redirects=True, ssl=False) as response:
                    if response.status == 200:
                        await ctx.send(selected_image)
                    else:
                        await ctx.send("Failed to retrieve Pepe image. Please try again later.")

        except FileNotFoundError:
            await ctx.send("pepe.txt file was not found, please make sure it's in the right directory.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")
