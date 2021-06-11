# bot.py
import os

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='faq', help='Searches the FAQ for the most relevant section corresponding to the provided keyword.')
async def faq(ctx, keyword):
    response = keyword
    await ctx.send(response)

bot.run(TOKEN)

'''
@bot.command(name='dailyreminder' help='Messages with daily reminders.')
async def dailyreminder(ctx, time, int:minsbefore, int:gmtplus):
    import time
'''
