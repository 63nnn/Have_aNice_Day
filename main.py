import discord as dc
from discord.ext import commands
import os
import json
from utils.system_const import SystemMessage as Sysmsg, SystemConst

with open("privateSetting.json", "r", encoding="utf8") as jfile:
    jj = json.load(jfile)

# bot
intents = dc.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


# bot get start
@bot.event
async def on_ready():
    await load_all_cmds()
    game = dc.CustomActivity("Playing ヨルシカ - 晴る")
    await bot.change_presence(status=dc.Status.online, activity=game)
    print(f"\n> > > Now log in: {bot.user} < < <")


# load cmds
@bot.command()
async def load(ctx, *extensions):
    if ctx.channel != bot.get_channel(jj["channelIDs"]["manager"]):
        await ctx.send(Sysmsg.PERMISSION_DENIED)
        return
    for extension in extensions:
        await bot.load_extension(f"cmds.{extension}")
        await ctx.send(f"Load {extension} done.")


# unload cmds
@bot.command()
async def unload(ctx, *extensions):
    if ctx.channel != bot.get_channel(jj["channelIDs"]["manager"]):
        await ctx.send(Sysmsg.PERMISSION_DENIED)
        return
    for extension in extensions:
        await bot.unload_extension(f"cmds.{extension}")
        await ctx.send(f"Unload {extension} done.")


# reload cmds
@bot.command()
async def reload(ctx, *extensions):
    if ctx.channel != bot.get_channel(jj["channelIDs"]["manager"]):
        await ctx.send(Sysmsg.PERMISSION_DENIED)
        return
    for extension in extensions:
        await bot.reload_extension(f"cmds.{extension}")
        await ctx.send(f"Reload {extension} done.")


# bot start function
async def load_all_cmds():
    print("\nstart loading...")
    for cmd in os.listdir("./cmds"):
        if cmd.endswith(".py"):
            try:
                await bot.load_extension(f"cmds.{cmd[:-3]}")
                print(f">> {cmd[:-3]:{15}} loaded successfully")
            except commands.ExtensionAlreadyLoaded:
                print(f">> {cmd[:-3]:{15}} already loaded")
            except Exception as e:
                print(f">> {cmd[:-3]:{15}} Error: \n\t{e}")


if __name__ == "__main__":
    from aiohttp import ClientConnectionError
    from dotenv import load_dotenv
    import time

    if not os.path.exists(".env"):
        print("Error occur: [.env] file not found.")
        exit(1)
    load_dotenv()

    while True:
        try:
            bot.run(os.getenv("TOKEN"))
        except ClientConnectionError:
            time.sleep(2)
        else:
            break
