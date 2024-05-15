import discord
from discord.ext import commands
import logging
import yaml
import random
import time
import re

# the config YAML is made globally available
global config
with open('./config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Setting intents
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = True

activity = discord.Activity(name="over this server", type=discord.ActivityType.watching)

bot = commands.Bot(
    command_prefix='$',
    intents=intents,
    activity=activity,
    shard_count=config['app']['discord_api']['shard_count'],
    shard_id=config['app']['discord_api']['shard_id']
    )

# Following lines set up the logger
handler = None
level = None
if config['app']['logging']['activate']:
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    level = str(config['app']['logging']['level'])
    # Alternative/backup logging (internal, using python3-logging)
    logging.basicConfig(level=level, handlers=[handler])

@bot.event
async def on_ready():
    print(f'Connected to Discord as {bot.user.name} with ID: {bot.user.id}')
    print(f'Running API version {discord.__version__}')
    print(f'Logging: {config["app"]["logging"]["activate"]}, Level: {level}')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong!\n\nI am a bot, logged in as "{bot.user.name}" with ID: {bot.user.id}.\nI am using the Discord API version {discord.__version__}.\nAnd how are you doing, human?')

@bot.command()
async def roll(ctx, die: str, amount: int):  # TODO Fix this! The code is garbage!
    number_characters = re.findall(r'\d+', die)
    if not number_characters:
        await ctx.send(f'"{die}" is not a valid dice.')
    sides = int(''.join(number_characters))
    output = []
    for roll in range(0, amount):
        result = random.randint(1, sides)
        output.append(result)
        
    await ctx.send(f'This is how you rolled:\n\n{' '.join(re.findall(r'\d+', str(output)))}')

# Custom help command, overriding the default help of discord.ext
class MyHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title='The Phantom Support',
            description="For meta information, refer to the documentation on https://github.com/caelestia-42bit/The_Phantom",
            color=discord.Color.brand_red()
        )
        embed.add_field(name='$help', value='The help command calls up this page, you are reading right now.', inline=False)
        embed.add_field(name='$roll <dice sides>', value='Roll a dice with a custom ammount of sides. Even weird ones ;)', inline=False)
        embed.add_field(name='$stop <admin password>', value='Stops the bot. Please dont show the password to everyone... Use an admin channel!', inline=False)
        embed.set_author(name='Caeleste', icon_url=None)

        await self.get_destination().send(embed=embed)
bot.help_command = MyHelpCommand()

bot.run(
    config['app']['discord_api']['token'],
    log_handler=handler,
    log_level=level
    )