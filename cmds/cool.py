"""
Currently despreted.
"""

from discord.ext import commands
import json

with open("setting.json", "r", encoding="utf8") as jfile:
    jj = json.load(jfile)


class Cool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def code(self, ctx):
        if ctx.channel == self.bot.get_channel(jj["weather"]):
            code = self.bot.get_channel(jj["sorce_code"])
            await code.send("It's repairring")


async def setup(bot):
    await bot.add_cog(Cool(bot))
