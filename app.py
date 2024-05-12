import discord
import json
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        print(f'CWD: {os.getcwd}')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
with open('~/.token', 'r') as tkn:
    token = json.load(tkn)
    tkn.close()

client.run()