from discord import *
import logging
import yaml
import os

global config
with open('./config.yaml', 'r') as file:
    config = yaml.safe_load(file)

intents = Intents.default()
intents.message_content = True
intents.typing = True
intents.members = True

activity = Activity(name="over this server", type=ActivityType.watching)

client = Client(intents = intents)

if(config['app']['discord_api']['logging']):
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
else:
    handler = None

@client.event
async def on_ready():
    print(f'Logged in as {client.user} with ID: {client.application_id}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    pass

client.run(config['app']['discord_api']['token'], log_handler=handler)