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

bot = commands.Bot(command_prefix="prm!",case_insensitive=True,activity=discord.Game('Beta | 導入数' + str(count), type=1))
token = os.environ['DISCORD_BOT_TOKEN']



    manage_cog.setup(bot)

bot.run(token)
