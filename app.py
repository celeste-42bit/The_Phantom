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


# ------------------ VtM Dice Roller ------------------

import random

NORMAL_EMOJIS = {
    "success": ":success:",
    "failure": ":fail:",
    "critical_failure": ":bestialfail:",
    "critical_success": ":crit:",
}

HUNGER_EMOJIS = {
    "success": ":redsuccess:",
    "failure": ":redfail:",
    "critical_failure": ":bestialfail:",  # same symbol
    "critical_success": ":redcrit:",
}

def eval_die(value: int) -> str:
    if value == 1:
        return "critical_failure"
    elif 2 <= value <= 5:
        return "failure"
    elif 6 <= value <= 9:
        return "success"
    elif value == 10:
        return "critical_success"

# -------------------------------------------------------------------------------------- DICE ROLLER --------------------------------------------------------------------------------
@bot.tree.command(name="roll", description="Roll Vampire: The Masquerade dice (d10 only)")
@discord.app_commands.describe(
    dice_amount="How many dice total?",
    hunger="How many hunger dice?"
)
async def roll(interaction: discord.Interaction, dice_amount: int, hunger: int):

    if dice_amount <= 0:
        return await interaction.response.send_message("You must roll at least 1 die.", ephemeral=True)

    if hunger < 0:
        return await interaction.response.send_message("Hunger cannot be negative.", ephemeral=True)

    if hunger > dice_amount:
        return await interaction.response.send_message("Hunger dice cannot exceed total dice.", ephemeral=True)

    normal_count = dice_amount - hunger

    normal_results = [eval_die(random.randint(1, 10)) for _ in range(normal_count)]
    hunger_results = [eval_die(random.randint(1, 10)) for _ in range(hunger)]

    output = []
    output.extend(NORMAL_EMOJIS[r] for r in normal_results)
    output.extend(HUNGER_EMOJIS[r] for r in hunger_results)

    final = " ".join(output)

    await interaction.response.send_message(final)
# -------------------------------------------------------------------------------------- DICE ROLLER --------------------------------------------------------------------------------


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