from discord.ext import commands


class Tool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        await ctx.send(err)

    @commands.command()
    async def purge(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)


async def setup(bot):
    await bot.add_cog(Tool(bot))
