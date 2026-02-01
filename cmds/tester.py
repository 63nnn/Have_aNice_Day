from discord.ext import commands
import discord
import asyncio
import pyperclip
from utils.system_const import SystemMessage, SystemConst
from datetime import datetime, timedelta, timezone


class Tester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def full_embed(self, ctx):
        embed = discord.Embed(
            title="📘 這是標題",
            description="這是描述內容，可以放多行文字，也支援 **Markdown** 語法。",
            color=discord.Color.blue(),
            timestamp=datetime.now(timezone(timedelta(hours=8))),  # 台灣時間
        )

        # 作者欄位（可加圖示）
        embed.set_author(
            name="Grok",
            icon_url="https://imgur.com/UUEUunF.png",
        )

        # 加入欄位（可以多個）
        embed.add_field(name="欄位 1", value="這是欄位內容", inline=True)
        embed.add_field(name="欄位 2", value="這也是欄位", inline=True)
        embed.add_field(name="欄位 3", value="這會自動換行", inline=False)

        # 設定縮圖（會顯示在右上角）
        embed.set_thumbnail(url="https://i.imgur.com/fKL31aD.jpg")

        # 設定主圖（會顯示在 embed 下方）
        embed.set_image(url="https://i.imgur.com/rdm3W9t.png")

        # 設定頁尾
        embed.set_footer(
            text="這是頁尾文字", icon_url="https://i.imgur.com/fKL31aD.jpg"
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def markdown_test(self, ctx):
        embed = discord.Embed(
            title="📘 Markdown 測試",
            description=(
                "**粗體文字**\n"
                "*斜體文字*\n"
                "__底線文字__\n"
                "`單行程式碼`\n"
                "```python\nprint('多行程式碼')\n```"
            ),
            color=discord.Color.blue(),
            timestamp=datetime.now(timezone(timedelta(hours=8))),
        )
        embed.set_footer(text="這是底部文字")
        await ctx.send(embed=embed)

    @commands.command()
    async def test_status(self, ctx, status):
        color_map = {
            "processing": SystemConst.EmbedColor.PROCESSING,
            "error": SystemConst.EmbedColor.ERROR,
            "warning": SystemConst.EmbedColor.WARNING,
            "success": SystemConst.EmbedColor.SUCCESS,
        }

        color = color_map.get(status.lower(), SystemConst.EmbedColor.WARNING)

        embed = discord.Embed(
            title=f"狀態：{status.capitalize()}",
            description="這是一個狀態測試的範例。",
            color=color,
            timestamp=datetime.now(timezone(timedelta(hours=8))),
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def process(self, ctx):
        try:
            # 創建初始嵌入訊息
            embed = discord.Embed(
                title="處理中", description="步驟 1/3", color=0xFFFF00
            )
            message = await ctx.send(embed=embed)

            # 更新進度
            await asyncio.sleep(2)
            embed.description = "步驟 2/3"
            await message.edit(embed=embed)

            await asyncio.sleep(2)
            embed.description = "步驟 3/3"
            await message.edit(embed=embed)

            await asyncio.sleep(2)

            # 刪除「處理中」訊息
            await message.delete()

            # 發送最終結果嵌入訊息
            final_embed = discord.Embed(
                title="完成", description="處理完成！結果：成功", color=0x00FF00
            )
            await ctx.send(embed=final_embed)

        except discord.Forbidden:
            await ctx.send("錯誤：我沒有權限編輯或刪除訊息！")
        except discord.NotFound:
            await ctx.send("錯誤：訊息已被刪除！")
        except Exception as e:
            await ctx.send(f"發生錯誤：{str(e)}")

    @commands.command()
    async def p2(self, ctx):
        try:
            # 創建初始嵌入
            embed = discord.Embed(
                title="處理中", description="步驟 1/3", color=discord.Colour.yellow()
            )
            message = await ctx.send(embed=embed)
            await message.add_reaction("⏳")  # 添加初始反應

            # 更新進度
            await asyncio.sleep(2)
            embed.description = "步驟 2/3"
            await message.edit(embed=embed)
            await message.remove_reaction("⏳", self.bot.user)
            await message.add_reaction("🔄")

            await asyncio.sleep(2)
            embed.description = "步驟 3/3"
            await message.edit(embed=embed)
            await message.remove_reaction("🔄", self.bot.user)
            await message.add_reaction("✅")

            # 刪除訊息並發送最終結果
            await asyncio.sleep(2)
            await message.delete()
            final_embed = discord.Embed(
                title="完成", description="結果：成功", color=discord.Colour.green()
            )
            final_embed.set_footer(text="完成時間")
            final_embed.timestamp = discord.utils.utcnow()
            await ctx.send(embed=final_embed)

        except discord.Forbidden:
            await ctx.send("錯誤：我沒有權限編輯、刪除訊息或管理反應！")
        except discord.NotFound:
            await ctx.send("錯誤：訊息已被刪除！")
        except Exception as e:
            await ctx.send(f"發生錯誤：{str(e)}")

    @commands.command()
    async def p3(self, ctx):
        from discord.ui import Button, View

        # 創建嵌入和按鈕
        embed = discord.Embed(
            title="處理中", description="步驟 1/3", color=discord.Colour.yellow()
        )
        view = View()
        button = Button(label="下一步", style=discord.ButtonStyle.primary)

        step = 1

        async def button_callback(interaction):
            nonlocal step
            step += 1
            if step <= 3:
                embed.description = f"步驟 {step}/3"
                await interaction.response.edit_message(embed=embed)
            else:
                await interaction.message.delete()
                final_embed = discord.Embed(
                    title="完成", description="結果：成功", color=discord.Colour.green()
                )
                await interaction.response.send_message(embed=final_embed)

        button.callback = button_callback
        view.add_item(button)

        # 發送初始訊息
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Tester(bot))
