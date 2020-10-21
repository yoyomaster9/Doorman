import discord
from discord.ext import commands
import config
import cogs

intents = discord.Intents.default()
intents.members = True

BOT_PREFIX = ','

bot = commands.Bot(command_prefix=BOT_PREFIX, intents = intents)
for x in commands.Cog.__subclasses__():
    bot.add_cog(x(bot))

@bot.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == bot.user:
        return

    # Purely administrative bot
    elif message.author.id != config.adminID:
        return

    # Otherwise process command
    else:
        await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print('---------------------')
    for g in bot.guilds:
        print('Logged into {}'.format(g))

if config.DiscordToken == 'Replace_with_token' or config.adminID == 12345:
    print('No config detected! Edit the config.py file.')
else:
    bot.run(config.DiscordToken)
