# Weather Cog

A cog for Redbot that provides weather information using the OpenWeatherMap API. Allows users to fetch current weather data for a specified city.

## Features

- **Set API Key:** Bot owner can set the OpenWeatherMap API key.
- **Get Weather:** Fetches and displays current weather data for a specified city.
- **Help Command:** Provides instructions on how to use the weather commands.

## Commands

- `!setweatherapikey <api_key>`: Sets the OpenWeatherMap API key for the bot owner.
<sub>You can get one from [OpenWeatherMap](https://home.openweathermap.org/api_keys).</sub>
- `!weather <CITY or ZIP>`: Will display weather, temp, highs/lows, and so on
- `!weather5day <CITY or ZIP>`: List the 5 day forecast

## Installation

1. **Download the repo with [Redbot](https://github.com/Cog-Creators/Red-DiscordBot)**
   ```[p]repo add DreamyCogs https://github.com/DreamyKiley/DreamyCogs```

2. **Install the cog**
   ```[p]cog install DreamyCogs weather```

3. **Load the cog**
   ```[p]load weather```

## Example

Here’s how the command works:

1. **Set API Key:**
   - Use `!setweatherapikey <api_key>` to set the API key.

2. **Fetch Weather:**
   - Use `!weather Brisbane` to get the weather data for the specified city.

## Support

For support or more information, visit [DreamyCogs GitHub](https://github.com/DreamyKiley).
