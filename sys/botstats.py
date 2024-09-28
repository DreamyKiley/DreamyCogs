import os
import platform
import psutil
import time
from discord import Embed
from redbot.core import commands, Config, checks

class BotStats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=156302847392649181)  # Unique Identifier to not interefere with other Red cogs

    @commands.command(name="sys")
    @checks.is_owner()
    async def system_stats(self, ctx: commands.Context):
        """Displays the system's CPU, RAM utilization, disk I/O, uptime, and ping to Discord."""
        # System-wide CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        # System-wide RAM usage
        ram_info = psutil.virtual_memory()
        ram_usage = ram_info.percent
        total_ram = ram_info.total / (1024 ** 3)  # Bytes to GB
        used_ram = ram_info.used / (1024 ** 3)    # Bytes to GB

        # Disk I/O (total since boot)
        disk_io = psutil.disk_io_counters()
        read_gb = disk_io.read_bytes / (1024 ** 3)  # Convert to GB
        write_gb = disk_io.write_bytes / (1024 ** 3)  # Convert to GB

        # System Uptime
        uptime_seconds = time.time() - psutil.boot_time()
        days, remainder = divmod(uptime_seconds, 86400)  # 86400 seconds in a day
        hours, remainder = divmod(remainder, 3600)  # 3600 seconds in an hour
        minutes, _ = divmod(remainder, 60)  # 60 seconds in a minute

        # Format uptime string
        uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m"

        # Measure ping to Discord
        ping = self.bot.latency * 1000  # Convert to milliseconds

        # Embed message
        embed = Embed(
            title="System Stats",
            # color=0x003B00  # Matrix green color
            color=0x00FF00  # green color
        )
        embed.description = "Powered by [DreamyCogs](https://github.com/DreamyKiley/DreamyCogs)"
        # Comment out what you don't want/need, I did this for my personal use mostly but sharing regardless
        embed.add_field(name="CPU Usage", value=f"{cpu_usage:>5.1f}%", inline=True)
        embed.add_field(name="RAM Usage", value=f"{ram_usage:>5.1f}% ({used_ram:>5.2f} GB / {total_ram:.2f} GB)", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)  # Empty field to break the line
        embed.add_field(name="Disk Read", value=f"{read_gb:>5.2f} GB", inline=True)
        embed.add_field(name="Disk Write", value=f"{write_gb:>5.2f} GB", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)  # Empty field for alignment
        embed.add_field(name="Uptime", value=f"{uptime_str}", inline=True)  # Uptime
        embed.add_field(name="Ping", value=f"{ping:.0f} ms", inline=True)  # Ping
        embed.add_field(name="\u200B", value="\u200B", inline=True)  # Empty field for alignment

        await ctx.send(embed=embed)

    @commands.command(name="sysrestart")
    @checks.is_owner()
    async def sys_restart(self, ctx: commands.Context):
        await ctx.send("Restarting the server...")

        # Platform-specific restart commands
        if platform.system() == "Windows":
            os.system("shutdown /r /t 1")  # Windows restart
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            os.system("sudo reboot")  # Linux or macOS restart
        else:
            await ctx.send("Unsupported OS for restart command.")
