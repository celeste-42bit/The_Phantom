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

# Following lines set up the logger
activate_logging = config['app']['logging']['activate']
logging_level = str(config['app']['logging']['level'])

try:
    if(activate_logging):
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    else:
        handler = None

    match logging_level:
        case "DEBUG":
            log_level = logging.DEBUG
        case "INFO":
            log_level = logging.INFO
        case "WARN":
            log_level = logging.WARNING
        case "ERROR":
            log_level = logging.ERROR
        case "CRIT":
            log_level = logging.CRITICAL

except:
    print('There is an issue with the config.yaml file. Please check thy syntax!')
    print('Logging has been disabled!')
    handler = None
    log_level = logging.INFO

# Successful connection to Discord
@client.event
async def on_ready():
    print(f'Logged in as {client.user} with ID: {client.application_id}')

# Received message in any chat
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    pass

client.run(
    config['app']['discord_api']['token'],
    log_handler=handler,
    log_level=log_level
    )