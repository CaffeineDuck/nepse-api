from discord.ext import commands

from nepse import Client

bot = commands.Bot(command_prefix="?")


class Nepse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nepse_client = Client()

    @commands.command()
    async def checkipo(self, ctx, scrip: str, boid: int):
        result = await self.nepse_client.market_client.check_IPO(scrip, boid)
        alloted = "Alloted" if result else "Not Alloted"

        await ctx.send(alloted)


bot.add_cog(Nepse(bot))

bot.run("YOUR_TOKEN_HERE")
