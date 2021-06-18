# coding: utf-8
from discord.ext import commands
import os
import traceback
import discord

discord_intents = discord.Intents.all()

class FetchUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

# from dotenv import load_dotenv
# load_dotenv()

bot = commands.Bot(command_prefix="pg!",case_insensitive=True,activity=discord.Game("pg!help" + " | " + "Pre-Alpha"))
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print('ログインしたよ～')
    print('-------------------')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------')

    manage_cog.setup(bot)

bot.run(TOKEN)
