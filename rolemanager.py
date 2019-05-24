from discord.ext import commands
import cogs.manage as manage_cog
import os

from dotenv import load_dotenv
load_dotenv()

# Bot token
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('ログインしたにゃ')
    print('-------------------')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------')

    manage_cog.setup(bot)

bot.run(TOKEN)