from discord.ext import commands
import discord
from datetime import datetime, timedelta, timezone
from utils.grok_service import GrokService
from utils.system_const import SystemMessage as Sysmsg, SystemConst
from utils.grok_response_embed import GrokResponseEmbed
import json


class Grok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__channel = None
        self.client = GrokService()
        self.usage = Sysmsg.GROK_USAGE

    def set_channel(self, channel):
        self.__channel = self.bot.get_channel(channel)

    @commands.group(name="grok", invoke_without_command=True)
    async def grok(self, ctx: commands.Context, *, prompt: str = None):
        # Usage 查詢
        if prompt == None or prompt.lower() == "usage":
            await ctx.send(embed=GrokResponseEmbed().simple_chat(answer=self.usage))
            return

        # 簡易問題形式
        async with ctx.channel.typing():
            response = await self.client.chat_completion(
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )
            await ctx.send(
                embed=GrokResponseEmbed().simple_chat(
                    question=prompt,
                    answer=response.choices[0].message.content,
                )
            )

    # Configure Model
    @grok.group(name="model", invoke_without_command=True)
    async def model(self, ctx):
        async with ctx.channel.typing():
            models: dict = None

            # 嘗試從 JSON 文件中讀取模型列表
            with open("./data/docs/grok_data.json", "r") as f:
                data = json.load(f)
                models: dict = data["grok_models"]

            # 如果模型列表仍然為空
            if models is None:
                await ctx.send(
                    embed=GrokResponseEmbed().system_message(message="無法獲取模型列表")
                )
                return

            await ctx.send(embed=GrokResponseEmbed().model_list(models=models))

    # Refresh Model
    @model.command()
    async def refresh(self, ctx):
        async with ctx.channel.typing():
            models = await self.client.get_models_list()
            if models is None:
                await ctx.send(
                    embed=GrokResponseEmbed().system_message(message="無法獲取模型列表")
                )
                return

            await ctx.send(embed=GrokResponseEmbed().model_list(models=models))

    # Set Model
    @model.command()
    async def set(self, ctx, model_select: str):
        async with ctx.channel.typing():
            response = await self.client.set_model(model_select)
            if response == None:
                await ctx.send(
                    embed=GrokResponseEmbed().simple_chat(
                        question="模型設定成功", answer=f"現在模型為: {model_select}"
                    )
                )
            else:
                await ctx.send(embed=GrokResponseEmbed().system_message(response))

    # Get Client Info
    @grok.command()
    async def info(self, ctx):
        async with ctx.channel.typing():
            client_info = await self.client.fetch_client_info()
            if client_info is None:
                await ctx.send("無法獲取客戶端資訊")
                return

            # 將客戶端資訊轉換為字串
            info_list = [
                f"模型: {client_info['model']}",
                f"API URL: {client_info['base_url']}",
                f"上次請求時間: {client_info['last_request_time']}",
            ]
            await ctx.send(
                embed=GrokResponseEmbed().simple_chat(
                    question="客戶端資訊",
                    answer=f"\n".join(info_list),
                )
            )

    # embed test
    @grok.command()
    async def edt(self, ctx, message):
        await ctx.send("embed=embed")

    @commands.Cog.listener()
    async def on_message(self, message):
        dontResponse = [
            message.author == self.bot.user,
            message.channel != self.__channel,
        ]
        if any(dontResponse):
            return

        pass  # TODO: Grok api

    #
    async def cog_unload(self):
        await self.client.close()  # 釋放 grok client 資源


async def setup(bot):
    with open("privateSetting.json", "r", encoding="utf8") as jfile:
        jj = json.load(jfile)
        channel = jj["channelIDs"]["grok"]

    ass = Grok(bot)
    ass.set_channel(channel=channel)
    await bot.add_cog(ass)
