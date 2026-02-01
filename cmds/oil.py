import asyncio

from discord.ext import commands, tasks
from datetime import datetime, timedelta
from utils.oil_service import OilService


class Oil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__channel = None
        self.oil_service: OilService = OilService()
        self.report_times = [
            {"weekday": 4, "hour": 12, "minute": 0},  # 每週五 12:00
            {"weekday": 6, "hour": 12, "minute": 0},  # 每週日 12:00
        ]
        self.oil_week_report.start()

    def set_channel(self, channel):
        self.__channel = self.bot.get_channel(channel)

    @commands.group(name="oil", invoke_without_command=True)
    async def oil(self, ctx: commands.Context):
        async with ctx.typing():
            self.oil_service.refresh()
            await ctx.send(embed=self.oil_service.dc_embed())

    @oil.command()
    async def refresh(self, ctx: commands.Context):
        async with ctx.typing():
            self.oil_service.refresh(enforce=True)
            await ctx.send(embed=self.oil_service.dc_embed())

    @tasks.loop(seconds=1)  # 我們手動控制 sleep 時間
    async def oil_week_report(self):
        if not self.__channel:
            print("Channel Setting Not Success.")
            return

        now = datetime.now()

        # 找出下一個排程時間
        next_run = None
        for i in range(7):  # 最多找一週內的時間
            day = (now + timedelta(days=i)).date()
            for time_config in self.report_times:
                if day.weekday() == time_config["weekday"]:
                    scheduled_time = datetime.combine(day, datetime.min.time()).replace(
                        hour=time_config["hour"], minute=time_config["minute"]
                    )
                    if scheduled_time > now:
                        if next_run is None or scheduled_time < next_run:
                            next_run = scheduled_time

        # 等待直到下次排程
        wait_seconds = (next_run - now).total_seconds()
        print(f"⏳ Next oil report will run in {wait_seconds / 3600:.2f} hours.")

        await asyncio.sleep(wait_seconds)

        self.oil_service.refresh()
        await self.__channel.send(embed=self.oil_service.dc_embed())

    @oil_week_report.before_loop
    async def before_weekly_task(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    import json

    with open("privateSetting.json", "r", encoding="utf8") as jfile:
        jj = json.load(jfile)
        channel = jj["channelIDs"]["oil"]

    oil = Oil(bot)
    oil.set_channel(channel)
    await bot.add_cog(oil)
