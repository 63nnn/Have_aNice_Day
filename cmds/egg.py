import discord as dc
from discord.ext import commands
import json
import os
import random

with open("setting.json", "r", encoding="utf8") as jfile:
    jj = json.load(jfile)


def includStr(seed: list, checked: str):
    for s in seed:
        for x in range(0, len(checked) - len(s) + 1):
            if checked.endswith(s, x, x + len(s)):
                return True
    return False


class Egg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_path = "./data/egg"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # owo
        if message.content in jj["owo"]:
            pass

        # inaff
        if includStr(jj["inaff"], message.content):
            inaff = []
            for file in os.listdir(f"{self.base_path}/inaff"):
                inaff.append(file)
            rand_inaff = random.choice(inaff)
            await message.channel.send(
                file=dc.File(f"{self.base_path}/inaff/{rand_inaff}")
            )
            return

        # uww
        if includStr(jj["uwu"], message.content):
            uwu = []
            for file in os.listdir(f"{self.base_path}/UWU"):
                uwu.append(file)
            rand_uwu = random.choice(uwu)
            await message.channel.send(file=dc.File(f"{self.base_path}/UWU/{rand_uwu}"))

        # inana
        if message.content == "inana":
            await message.delete()
            await message.channel.send(file=dc.File(f"{self.base_path}/inana/ina.gif"))

        # ahoy
        if includStr(jj["ahoy"], message.content):
            ahoy = []
            for file in os.listdir(f"{self.base_path}/ahoy"):
                ahoy.append(file)
            rand_ahoy = random.choice(ahoy)
            await message.channel.send(
                file=dc.File(f"{self.base_path}/ahoy/{rand_ahoy}")
            )

        # peko
        if includStr(jj["peko"], message.content):
            await message.channel.send("2025 誰還在 peko??")


async def setup(bot):
    await bot.add_cog(Egg(bot))
