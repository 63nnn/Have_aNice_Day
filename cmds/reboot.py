"""
Currently despreted
"""

from discord.ext import tasks, commands
from datetime import datetime, timezone, timedelta
import os


class reboot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(979984383912071218)
        self.reboot.start()
        self.counter = True
        self.time = "0000"

    @tasks.loop(seconds=60.0)
    async def reboot(self):
        localT = datetime.utcnow().replace(tzinfo=timezone.utc)
        utc8 = localT.astimezone(timezone(timedelta(hours=8)))
        nowT = utc8.strftime("%H%M")
        if nowT == self.time and self.counter:
            await self.channel.send("reboot success")
            os.system("kill 1")
            self.counter = False
        else:
            pass

    @reboot.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(reboot(bot))
