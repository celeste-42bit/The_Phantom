import discord
from discord.ext import commands
import logging
import yaml
import random
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

command_prefix = '$'
activity = discord.Activity(name="over this server", type=discord.ActivityType.watching)
status = discord.Status.online

bot = commands.Bot(
    command_prefix = command_prefix,
    intents = intents,
    activity = activity,
    stauts = status,
    case_insensitive = True,
    owner_id = ['456175197415014403', '287663053707673600'],  # caelestia-42bit (https://github.com/caelestia-42bit), ShaeCalmine
    shard_count = config['app']['discord_api']['shard_count'],
    shard_id = config['app']['discord_api']['shard_id']
    )

# Set up the logger (logging and internal)
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
    logging.debug(config)

# ping the bot
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong!\n\nI am a bot, logged in as "{bot.user.name}" with ID: {bot.user.id}.\nI am using the Discord API version {discord.__version__}.\nAnd how are you doing, human?')
    logging.info('PING!')

# roll custom ammount of multi-sided dice
@bot.command(name='roll')
async def roll(ctx, die: str, amount: int):
    # TODO There is an issue with conversion. re.findall returns a list. Int is needed!
    number_characters = re.findall(r'\d+', die)

    if not number_characters or number_characters < 2:  # Comparison only works between congruent types!!! (Error: list < int)
        await ctx.send(f'"{die}" is not a valid dice.')
        return

    sides = int(''.join(number_characters))
    output = []
    for result in range(0, amount):  # TODO is that correct?!?!?!
        result = random.randint(1, sides)
        output.append(result)
    # TODO SyntaxError: unexpected character after line continuation character
    output = re.findall(r'\d+', str(output))
    output = ''.join(output)
    await ctx.send(f'This is how you rolled:\n\n{output}')

# change bot activity
@bot.command(name='chact')
async def chact(ctx, activity):
    try:
        bot.activity = discord.Activity(name=activity, type=discord.ActivityType.custom)
    except:
        await ctx.send(f'ERROR: Failed to change the {bot.user.name}\'s activity.')
        logging.error(f'Failed to process chactivity request by {ctx.user.name}')

    await ctx.send(f'Changed {bot.user.name}\'s activity to: "{activity}"')
    logging.info(f'{ctx.user.name} changed {bot.user.name}\'s activity to: "{activity}"')

# change bot status
@bot.command(name='chst')
async def chst(ctx, status):
    try:
        match status:
            case "dnd":
                bot.status = discord.Status.dnd
            case "online":
                bot.status = discord.Status.online
            case "offline":
                bot.status = discord.Status.offline
            case "idle":
                bot.status = discord.Status.idle
    except:
        await ctx.send(f'There was an issue with setting {bot.user.name}\'s status to "{status}"')
        return

# Shutdown bot (owner)
@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send(f'{ctx.user.name} issued the bot.close() command. Shutting down!')
    logging.info(f'{ctx.user.name} issued the bot.close() command.')
    logging.shutdown
    await bot.close()

# Custom help command, overriding the default help of discord.ext
class MyHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title=f'{bot.user.name}',
            description="For meta information, refer to the documentation on https://github.com/caelestia-42bit/The_Phantom",
            color=discord.Color.brand_red(),
            url=None,
        )
        embed.add_field(
            name=f'{command_prefix}help',
            value='The help command calls up this page, you are reading right now.',
            inline=True
            )
        embed.add_field(
            name=f'{command_prefix}ping',
            value='Pokes the bot...',
            inline=True
            )
        embed.add_field(
            name=f'{command_prefix}roll <dice sides>',
            value='Roll a dice with a custom ammount of sides. Even weird ones ;)',
            inline=True
            )
        embed.add_field(
            name=f'{command_prefix}stop <admin password>',
            value='Stops the bot. Please dont show the password to everyone... Use an admin channel!',
            inline=True
            )
        embed.add_field(
            name=f'{command_prefix}chact <activity>',
            value='Changes the bots activity callout.',
            inline=True
            )
        embed.add_field(
            name=f'{command_prefix}chst <status>',
            value='Changes the bots status. Select either online, offline, idle, or dnd.',
            inline=True
            )
        embed.set_author(
            name=f'Created by The Phantasm Bot Projects',
            icon_url=None
            )

        await self.get_destination().send(embed=embed)
bot.help_command = MyHelpCommand()

bot.run(
    config['app']['discord_api']['token'],
    log_handler=handler,
    log_level=level
    )