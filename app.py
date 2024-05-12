import discord
import yaml
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        print(f'CWD: {os.getcwd}')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

global config
with open('./config.yaml', 'r') as file:
    config = yaml.safe_load(file)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(config['app']['api']['token'])