# --------------------------------------------------
# The Phantom Discord Bot
# By: celeste-42bit & The Phantasm Bot Projects
# Project date: 17/04/2025
# License: (C) 2020-2025 celeste-42bit; MIT
# --------------------------------------------------

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

command_prefix = '/'
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
description = ''
activity = discord.Activity(name="over this server", type=discord.ActivityType.watching)
status = discord.Status.online

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or(command_prefix),
    intents = intents,
    activity = activity,
    stauts = status,
    case_insensitive = True,
    help_command = help_command,
    description = description,
    owner_id = ['456175197415014403', '287663053707673600'],  # celeste-42bit (https://github.com/celeste-42bit), ShaeCalmine
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
    return

# ping the bot
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong!\n\nI am a bot, logged in as "{bot.user.name}" with ID: {bot.user.id}.\nI am using the Discord API version {discord.__version__}.\nAnd how are you doing, human?')
    logging.info('PING!')
    return

@bot.command(name='cookie')
async def cookie(ctx, amount=1):
    cookies = []
    for _ in range(amount):
        cookies.append('🍪')
    await ctx.send(str(" ".join(cookies)))

@bot.command(name='parse')
async def parse(ctx, *args):
    await ctx.send(args)



# say hi
@bot.command(name='hi')
async def hi(ctx):
    await ctx.send(f'Hello, human!')

# test command, just for me
@bot.command(name='test')
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')



@bot.command(name='roll')
async def roll(ctx, *args):
    args = list(args)
    valid_dice = config['app']['dice_roller']['valid_dice']

    if len(args) != 2:  # must have 2 args
        await ctx.send('❌ Please provide 2 arguments. For example "/roll 5 d20"')
        return

    if not str(args[0]).isdigit():  # amount must be number
        await ctx.send(f'❌ You can\'t roll "{args[0]}" dice... obviously!')
        return

    amount = int(args[0])

    if not str(args[1]).startswith('d') or not str(args[1][1:]).isdigit():  # dice must start with 'd' followed by a number
        await ctx.send(f'❌ "{args[1]}" is not a valid dice. A dice starts with "d" followed by a number, like "d20"!')
        return

    dice_sides = int(args[1][1:])

    if amount < 1:  # prevent 0 dice
        await ctx.send('❌ Congrats, you rolled a critical NOTHING! 🥳')
        return

    if amount > config['app']['dice_roller']['max_dice_amount'] or amount > 1000:  # prevent absurd amounts of dice
        await ctx.send('❌ Whoaaa, chill buddy! That\'s a lot of dice!')
        return

    if dice_sides > 1000000:
        await ctx.send('❌ That\'s a lot of sides!')
        return

    if not valid_dice:  # if valid_dice is empty, just roll
        await ctx.send(f'{", ".join(map(str, roll_dice(amount, dice_sides)))}')
        return

    if dice_sides not in valid_dice:  # if valid_dice is not empty and the requested dice is not in valid_dice, error out
        valid_dice_message = ", ".join(map(str, config['app']['dice_roller']['valid_dice']))
        await ctx.send(f'❌ The GM is a boring person and only allows d{valid_dice_message}.')
        return

    await ctx.send(f'{", ".join(map(str, roll_dice(amount, dice_sides)))}')

def roll_dice(amount: int, dice_sides: int):
    return [random.randint(1, dice_sides) for _ in range(amount)]


# Shutdown bot (owner)
@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send(f'{ctx.user.name} issued the bot.close() command. Shutting down!')
    logging.info(f'{ctx.user.name} issued the bot.close() command.')
    logging.shutdown
    await bot.close()

'''
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
            value='The help command calls up this page, you are reading right now. Duh.',
            inline=True
            )
        embed.add_field(
            name=f'{command_prefix}ping',
            value='Poke the bot...',
            inline=True
            )
        embed.add_field(
            name=f'{command_prefix}roll <dice amount> <dice type>',
            value=f'Roll a dice. A diece begins with "d" followed by one of the following numbers of sides: {", ".join(map(str, config["app"]["dice_roller"]["valid_dice"]))}',
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
'''

if __name__ == "__main__":
    print('running...')
    bot.run(
        config['app']['discord_api']['token'],
        log_handler=handler,
        log_level=level
        )