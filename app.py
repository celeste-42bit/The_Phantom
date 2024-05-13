import discord
from discord.ext import commands
import logging
import yaml
import os

# the config YAML is made globally available
global config
with open('./config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Setting intents ('default()' enables defaults intents and keeps privileged intents disabled)
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = True

activity = discord.Activity(name="over this server", type=discord.ActivityType.watching)

bot = commands.Bot(command_prefix='$', intents=intents)

# Following lines set up the logger
activate_logger = config['app']['logging']['activate']
level = str(config['app']['logging']['level'])


if activate_logger:
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    logging.basicConfig(level=level, handlers=[handler])


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong!\n\nI am a bot, logged in as {bot.user.name} with ID: {bot.user.id}.\nI am using the Discord API version {discord.__version__}.\nAnd how are you doing, human?')

@bot.event
async def on_ready():
    print(f'Connected to Discord as {bot.user.name} with ID: {bot.user.id}')
    print(f'Running API version {discord.__version__}')

bot.run(config['app']['discord_api']['token'])

# Run
#client.run(
#    config['app']['discord_api']['token'],
#    log_handler=handler,
#    log_level=log_level
#    )