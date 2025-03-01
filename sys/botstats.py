import os
import platform
import psutil
import time
from discord import Embed
from redbot.core import commands, Config, checks

ALLOWED_USERS = {XXXXXXXXXXXXXXX, YYYYYYYYYYYYY, ZZZZZZZZZZZZ}  # Replace with Discord user IDs

class BotStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=156302847392649181)

    @commands.command(name="sys")
    async def system_stats(self, ctx: commands.Context):
        """Displays the system's CPU, RAM utilization, disk I/O, uptime, and ping to Discord."""
        if ctx.guild is None and ctx.author.id not in ALLOWED_USERS:
            await ctx.send("You are not authorized to use this command.")
            return

        cpu_usage = psutil.cpu_percent(interval=1)
        ram_info = psutil.virtual_memory()
        ram_usage = ram_info.percent
        total_ram = ram_info.total / (1024 ** 3)  # Bytes to GB
        used_ram = ram_info.used / (1024 ** 3)    # Bytes to GB
        disk_io = psutil.disk_io_counters()
        read_gb = disk_io.read_bytes / (1024 ** 3)  # Convert to GB
        write_gb = disk_io.write_bytes / (1024 ** 3)  # Convert to GB
        uptime_seconds = time.time() - psutil.boot_time()
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)
        uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m"
        ping = self.bot.latency * 1000

        # embed stuff
        embed = Embed(title="System Stats", color=0x00FF00)  # Green
        embed.description = "Powered by [DreamyCogs](https://github.com/DreamyKiley/DreamyCogs)"
        embed.add_field(name="CPU Usage", value=f"{cpu_usage:>5.1f}%", inline=True)
        embed.add_field(name="RAM Usage", value=f"{ram_usage:>5.1f}% ({used_ram:>5.2f} GB / {total_ram:.2f} GB)", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)
        embed.add_field(name="Disk Read", value=f"{read_gb:>5.2f} GB", inline=True)
        embed.add_field(name="Disk Write", value=f"{write_gb:>5.2f} GB", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)
        embed.add_field(name="Uptime", value=f"{uptime_str}", inline=True)
        embed.add_field(name="Ping", value=f"{ping:.0f} ms", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="sysrestart")
    async def sys_restart(self, ctx: commands.Context):
        """Restarts the system."""
        if ctx.guild is None and ctx.author.id not in ALLOWED_USERS:
            await ctx.send("You are not authorized to use this command.")
            return

        await ctx.send("Restarting the server...")

        if platform.system() == "Windows":
            os.system("shutdown /r /t 1")  # Windows restart
        elif platform.system() in ["Linux", "Darwin"]:
            os.system("sudo reboot")  # Linux or macOS restart
        else:
            await ctx.send("Unsupported OS for restart command.")

    @commands.command(name="sysdisk")
    async def system_disk_stats(self, ctx: commands.Context):
        """Displays detailed disk usage per drive."""
        if ctx.guild is None and ctx.author.id not in ALLOWED_USERS:
            await ctx.send("You are not authorized to use this command.")
            return

        embed = Embed(title="Disk Usage", color=0x00FF00)
        embed.description = "Powered by [DreamyCogs](https://github.com/DreamyKiley/DreamyCogs)"

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total_gb = usage.total / (1024 ** 3)
                used_gb = usage.used / (1024 ** 3)
                free_gb = usage.free / (1024 ** 3)
                usage_percent = usage.percent
                
                embed.add_field(name=f"Drive {partition.device}", 
                                value=f"Used: {used_gb:.2f} GB / {total_gb:.2f} GB\nFree: {free_gb:.2f} GB\nUsage: {usage_percent:.1f}%", 
                                inline=False)
            except PermissionError:
                continue

        await ctx.send(embed=embed)
