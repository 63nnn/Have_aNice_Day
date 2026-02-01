from discord.ext import commands
from datetime import datetime, timedelta, timezone
import json


with open("privateSetting.json", "r", encoding="utf8") as jfile:
    jj = json.load(jfile)


def dateTimeString():
    # 計算 UTC+8 時間並減去 20 分鐘
    dt = datetime.now(timezone(timedelta(hours=8))) - timedelta(minutes=20)

    # 將分鐘取整到最近的 10 分鐘
    minutes = (dt.minute // 10) * 10
    dt = dt.replace(minute=minutes, second=0, microsecond=0)

    # 格式化為 YYYYMMDDHHMM
    return dt.strftime("%Y%m%d%H%M")


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__channel = None

    def set_channel(self, channel):
        self.__channel = self.bot.get_channel(channel)

    # set command group
    @commands.group(invoke_without_command=True)
    async def weather(self, ctx):
        await ctx.send("Please use `weather <command>`")

    @weather.command()
    async def radar(self, ctx):
        time_str = dateTimeString()
        await ctx.send(f"https://www.cwa.gov.tw/Data/radar/CV1_3600_{time_str}.png")

    # old weather command
    @commands.command()
    async def w(self, ctx):
        if ctx.channel == self.__channel:
            time_str = dateTimeString()
        if ctx.channel == self.__channel:
            time_str = dateTimeString()
            await ctx.send(f"https://www.cwa.gov.tw/Data/radar/CV1_3600_{time_str}.png")
        else:
            await ctx.send("Please try again in WEATHER.")


async def setup(bot):
    weather = Weather(bot)
    weather.set_channel(channel=jj["channelIDs"]["weather"])
    await bot.add_cog(weather)
