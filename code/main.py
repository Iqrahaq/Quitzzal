# main.py

import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv
import traceback
import datetime

# Use dotenv to conceal token.
load_dotenv()

# Other necessary variables 
TOKEN = os.getenv('DISCORD_TOKEN')
ROLE = ""
MEMBERS = []
todays_date = datetime.date.today()


intents = discord.Intents.default()
intents.members = True

# Command prefix
client = commands.Bot(command_prefix='qq!', intents=intents)

# Helpful loading prompt.
print("Starting bot...")

# Remove default help command to allow for qq!help.
client.remove_command('help')

# Error checking...
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error. Try qq!help ({error})')
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# Load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# Set custom status for bot.
async def custom_status():
    if 3 <= todays_date.month <= 5:
        await client.change_presence(activity=discord.Game(name="🌱 Doing the next spring quiz 🌱"))
    elif 6 <= todays_date.month <= 8:
        await client.change_presence(activity=discord.Game(name="🌻 Doing the next summer quiz 🌻"))
    elif 9 <= todays_date.month <= 11:
        await client.change_presence(activity=discord.Game(name="🍂 Doing the next autumn quiz 🍂"))
    else:
        await client.change_presence(activity=discord.Game(name="❄️ Doing the next winter quiz ❄️"))

@client.event
async def on_ready():
    await custom_status()
    print(f'{client.user} has connected to Discord!')
    

# token
client.run(TOKEN, reconnect=True)
