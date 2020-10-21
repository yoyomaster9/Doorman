from discord.ext import commands

class Utilties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = 'Checks to see if the bot is responsive',
                    help = 'Responds with Pong!',
                    brief = 'Responds with Pong!')
    async def ping(self, ctx):
        await ctx.send('Pong! {}ms'.format(round(self.bot.latency*1000, 1)))

    @commands.command(brief = 'Logs out of all servers.',
                    description  = 'Logs out of all servers.')
    async def logout(self, ctx):
        await ctx.send('Logging out!!')
        await self.bot.logout()
