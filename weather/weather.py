import aiohttp
from redbot.core import commands, Config
from discord import Embed
from datetime import datetime, timedelta

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=502837649120374658)
        self.config.register_global(api_key=None)  # Register global API key

    async def fetch_data(self, url):
        """Fetches data from the API and returns the JSON response or raises an error."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    try:
                        return await response.json()
                    except Exception as e:
                        raise ValueError(f"Failed to parse data: {e}")
                status_messages = {
                    404: "City not found.",
                    401: "Invalid API key."
                }
                raise ValueError(status_messages.get(response.status, "An error occurred."))

    def format_time(self, timestamp, offset):
        """Formats the time based on UTC and timezone offset."""
        return (datetime.utcnow() + timedelta(seconds=offset)).strftime('%I:%M %p')

    def format_date(self, date_text):
        """Formats the date to exclude time."""
        return datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    async def get_api_key(self):
        """Retrieves the API key from the configuration."""
        api_key = await self.config.api_key()
        if not api_key:
            raise ValueError("The API key has not been set.")
        return api_key

    @commands.command(name="setweatherapikey")
    @commands.is_owner() 
    async def set_weather_api_key(self, ctx, *, api_key: str = None):
        """Sets the OpenWeatherMap API key for the bot owner."""
        if api_key:
            await self.config.api_key.set(api_key)
            await ctx.send("The API key has been set successfully.")
        else:
            await ctx.send("You need to provide an API key from [OpenWeatherMap](https://home.openweathermap.org/api_keys).")

    @commands.command(name="weather")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def get_weather(self, ctx, *, city: str = None):
        """Fetches the current weather for a specified city."""
        if not city:
            await ctx.send("You must include a city, e.g., !weather Brisbane")
            return

        try:
            api_key = await self.get_api_key()
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            data = await self.fetch_data(url)

            embed = Embed(
                title=f"Weather in {data['name']}, {data['sys']['country']} - {self.format_time(datetime.utcnow(), data['timezone'])}",
                description=(
                    f"**Condition:** {data['weather'][0]['description'].title()}\n"
                    f"**Temperature:** {data['main']['temp']}°C ({(data['main']['temp'] * 9/5) + 32:.1f}°F)\n"
                    f"**Feels Like:** {data['main']['feels_like']}°C ({(data['main']['feels_like'] * 9/5) + 32:.1f}°F)\n"
                    f"**Highs/Lows:** {data['main']['temp_max']}°C/{data['main']['temp_min']}°C ({(data['main']['temp_max'] * 9/5) + 32:.1f}°F/{(data['main']['temp_min'] * 9/5) + 32:.1f}°F)\n"
                    f"**Humidity:** {data['main']['humidity']}%\n\n"
                    f"[DreamyCogs](https://github.com/DreamyKiley/DreamyCogs/)\n\n"
                ),
                color=0x1E90FF
            )
            embed.set_footer(text="Powered by OpenWeatherMap")
            await ctx.send(embed=embed)
        except ValueError as e:
            await ctx.send(str(e))

    @commands.command(name="weather5day")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def get_weather_5day(self, ctx, *, city: str = None):
        """Fetches the 5-day weather forecast for a specified city."""
        if not city:
            await ctx.send("You must include a city, e.g., !weather5day Brisbane")
            return

        try:
            api_key = await self.get_api_key()
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            data = await self.fetch_data(url)

            embed = Embed(
                title=f"5-Day Weather Forecast in {data['city']['name']}, {data['city']['country']}",
                description="Here’s the 5-day forecast:",
                color=0x1E90FF
            )

            for forecast in data['list'][::8]:
                embed.add_field(
                    name=self.format_date(forecast['dt_txt']),
                    value=(
                        f"**Condition:** {forecast['weather'][0]['description'].title()}\n"
                        f"**Temperature:** {forecast['main']['temp']}°C\n\n"
                    ),
                    inline=False
                )

            embed.set_footer(text="Powered by OpenWeatherMap")
            await ctx.send(embed=embed)
        except ValueError as e:
            await ctx.send(str(e))

    @commands.command(name="weatherhelp")
    async def weather_help(self, ctx):
        """Provides information on how to use the weather command."""
        help_message = (
            "1. **Get the weather:**\n"
            "`!weather <city>`\n"
            "2. **Get the 5-day forecast:**\n"
            "`!weather5day <city>`\n"
            "For more information, visit [Created by Kiley W.](https://github.com/DreamyKiley)"
        )
        await ctx.send(help_message)
