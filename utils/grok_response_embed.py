from datetime import datetime, timedelta, timezone
from utils.system_const import SystemConst
import discord

MAX_TITLE_LENGTH: int = 256


class GrokResponseEmbed:
    """
    A class to represent a message embed with various fields.
    """

    def __init__(
        self,
        name: str = "Grok",
        icon: str = "https://imgur.com/UUEUunF.png",
        title: str = None,
        color: SystemConst.EmbedColor = None,
        timestamp=datetime.now(timezone(timedelta(hours=8))),  # 台灣時間
    ):
        self.name = name
        self.authIcon = icon
        self.titleText = title
        self.timestamp = timestamp

        # 建立 Embed 實體
        self.embed = discord.Embed(
            title=self.titleText,
            color=color,
            timestamp=self.timestamp,
        )
        self.embed.set_author(
            name=self.name,
            icon_url=self.authIcon,
        )

    def system_message(self, message: str = None):
        self.embed.title = "警告\n"
        self.embed.description = message
        self.embed.color = SystemConst.EmbedColor.WARNING
        return self.embed

    def simple_chat(
        self,
        question: str = None,
        answer: str = None,
    ):
        raw_title = (question or "").split()[0]  # 取第一行

        # 檢查是否超過限制
        if len(raw_title) > MAX_TITLE_LENGTH:
            raw_title = raw_title[: MAX_TITLE_LENGTH - 10] + "..."
        else:
            raw_title = raw_title

        self.embed.title = f"{raw_title or ""}\n"
        self.embed.description = answer
        self.embed.color = SystemConst.EmbedColor.GROK
        return self.embed

    def rich_chat(self, data: dict):
        pass

    def image_chat(self, data: dict):
        pass

    def model_list(self, models: dict):
        self.embed.title = "可用的模型列表\n"

        # 將模型列表轉換為字串
        model_list = [f"```{str(model)}```" for model in models.keys()]
        self.embed.description = "".join(model_list)
        return self.embed
