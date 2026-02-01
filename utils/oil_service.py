import requests
import discord

from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from utils.system_const import SystemConst, SystemMessage


class OilService:
    _oil_url = "https://gas.goodlife.tw/"

    def __init__(self):
        self.prices: dict = {}
        self.prices_adjust: str = ""
        self.error_message: str = ""
        self.last_time: defaultdict = defaultdict(lambda: datetime.min)

    def get_soup(self) -> BeautifulSoup:
        self.error_message = ""
        try:
            html = requests.get(self._oil_url)
            html.raise_for_status()
        except Exception as e:
            self.error_message = str(e)
            return None

        soup = BeautifulSoup(html.content, "html.parser", from_encoding="utf-8")
        return soup

    def get_oil_price(self, enforce: bool = False):
        # 油價
        oil_items = ["92", "95", "98"]

        if not self.check_date_same("prices") or self.prices == {} or enforce:
            soup = self.get_soup()
            if soup:
                cpc_div = soup.find_all("div", id="cpc")[0]
                self.prices["title"] = cpc_div.find("h2").text.strip()
                oil_prices = cpc_div.find_all("li")

                # 成功會有 4 項
                if len(oil_prices) == 4:
                    for index, li in enumerate(oil_prices[:3]):  # 不用柴油
                        name = li.find("h3").text
                        if oil_items[index] in name:
                            price = li.get_text().replace(name, "").strip()
                            self.prices[oil_items[index]] = price
        return self.prices

    def get_next_week_adjust(self, enforce: bool = False):
        if (
            not self.check_date_same("prices_adjust")
            or self.prices_adjust == ""
            or enforce
        ):
            soup = self.get_soup()
            if soup:
                data: list = (list)(soup.find("li", class_="main").text.split())
                self.prices_adjust = ""

                # 網站可能的變化 TODO: 還沒看過
                if len(data) == 3:  # 禮拜一
                    self.prices_adjust = data[1] + data[2]
                elif len(data) > 9 and data[9] == "不":
                    self.prices_adjust = "周一汽油每公升不調整"
                else:
                    for i in range(len(data) - 1):
                        self.prices_adjust += data[i]
        return self.prices_adjust

    def check_date_same(self, target: str) -> bool:
        today = datetime.now()
        if today.date() == self.last_time[target].date():
            return True
        else:
            self.last_time[target] = today
            return False

    def refresh(self, enforce: bool = False):
        self.get_oil_price(enforce=enforce)
        self.get_next_week_adjust(enforce=enforce)

    def dc_embed(self):

        color = SystemConst.OilColor.UNKNOWN
        titleHint = ""
        if "漲" in self.prices_adjust:
            color = SystemConst.OilColor.RISE
            titleHint = "<漲>"
        elif "降" in self.prices_adjust:
            color = SystemConst.OilColor.FALL
            titleHint = "<降>"
        else:
            color = SystemConst.OilColor.STABLE
            titleHint = "<不調整>"

        # 建立 Embed 實體
        embed = discord.Embed(
            title=f"油價公告\t {titleHint}",
            color=color,
            timestamp=datetime.now(timezone(timedelta(hours=8))),
        )
        embed.description = SystemMessage.Oil_PRICE_TEMPLATE.format(
            title=self.prices["title"],
            p92=self.prices["92"],
            p95=self.prices["95"],
            p98=self.prices["98"],
            week_adjust=self.prices_adjust,
            error_message=self.error_message,
        )

        # Source
        embed.description += f"\nSource: {self._oil_url}"

        return embed
