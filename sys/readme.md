# System Stats Cog

A cog for Redbot that provides real-time system statistics, including CPU and RAM usage, disk I/O, uptime, and bot ping to Discord. This information is accessible to the bot owner only.

## Features

- **CPU Usage:** Displays the current CPU usage percentage.
- **RAM Usage:** Shows the percentage of RAM used along with total and used RAM in GB.
- **Disk I/O:** Reports the total amount of data read from and written to disk since boot.
- **Uptime:** Displays the system's uptime in days, hours, and minutes.
- **Ping:** Measures the bot's ping to Discord in milliseconds.
- **Command:**
  - `!sys`: Displays the system statistics.
  - `!sysdisk`: Displays the total disk usage across drives.
  - `!sysrestart`: Restarts your host machine.

## Installation

1. **Download the repo with [Redbot](https://github.com/Cog-Creators/Red-DiscordBot)**
   ```[p]repo add DreamyCogs https://github.com/DreamyKiley/DreamyCogs```

2. **Install the cog**
   ```[p]cog install DreamyCogs sys```

3. **Load the cog**
   ```[p]load sys```

## Commands

### `!sys`
Displays the system's CPU usage, RAM usage, disk I/O, uptime, and ping to Discord. This command is available only to the bot owner.

## Example

Here’s how the command works:

1. **Run the Command:**
   - Use `!sys` to get a summary of your server machine's system statistics.

2. **View the Stats:**
   - The bot will send an embed message with the following information:
     - **CPU Usage:** Current CPU usage percentage.
     - **RAM Usage:** RAM usage percentage and total/used RAM in GB.
     - **Disk Read/Write:** Total GB read from and written to disk.
     - **Uptime:** System uptime formatted as days, hours, and minutes.
     - **Ping:** Server latency to Discord in milliseconds.

## Support

For support or more information, visit [DreamyCogs GitHub](https://github.com/DreamyKiley).
