import discord
import os
import json
import asyncio
import random
import requests
from datetime import datetime
from Consolly import consoler
from bot.configdb import config_db
console = consoler()

class bot_core:
    def __init__(self):
        self.path = None

    async def cogload(self, bot):
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                await bot.load_extension(f'commands.{filename[:-3]}')

    async def anim_presence(self, bot):
        with open('bot.json') as f:
            data = json.load(f)

        await bot.wait_until_ready()
        
        while not bot.is_closed():
            await bot.change_presence(activity=discord.Game(name=random.choice(data['status'])))
            await asyncio.sleep(10)

    def roleapi(self, category: str=None, type: str=None):
        img_type = ['gif', 'png']
        gif_type = ['baka', 'bite', 'blush', 'bored', 'cry', 'cuddle', 'dance', 'facepalm', 'feed', 'handhold', 'happy', 'highfive', 'hug', 'kick', 'kiss', 'laugh', 'pat', 'poke', 'pout', 'punch', 'shoot', 'shrug', 'slap', 'sleep', 'smile', 'smug', 'stare', 'think', 'thumbsup', 'tickle', 'wave', 'wink', 'yeet']
        base_url = 'https://nekos.best/api/v2'

        if type in img_type:
            if type == 'gif':
                if category in gif_type:
                    d = []
                    data = requests.get(base_url + '/' + category).json()
                    d.append(data['results'][0]['url'])
                    d.append(data['results'][0]['anime_name'])
                    return d

    def get_language(self, id, category: str, file: str=None):
        with open('bot/db/{}.json'.format(id)) as f:
            data = json.load(f)
        
        with open('bot/Languages/role.json') as f:
            languages = json.load(f)

        if data['server']['language'] == 'english':
            return f'{languages["english"][category]}'
        else:
            return f'{languages["spanish"][category]}'

    def server_config(self, id):
        with open('bot/db/{}.json'.format(id)) as f:
            data = json.load(f)

        return data

    def return_embed_color(self, id):
        with open('bot/db/{}.json'.format(id)) as f:
            data = json.load(f)
        
        return int(data['server']['embed_color'], 16)

    def get_token(self):
        try:
            with open('bot.json') as f:
                settings = json.load(f)
            
            console.clear()
            return settings['huromi']['token']
        except FileNotFoundError:
            print(f'[{datetime.today().month}/{datetime.today().day}/{datetime.today().year} - {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}] To use this bot you need to create one and get the token you can get it at \n[{datetime.today().month}/{datetime.today().day}/{datetime.today().year} - {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}] https://discord.com/developers/applications\n[{datetime.today().month}/{datetime.today().day}/{datetime.today().year} - {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}] Once you have it, enter the token at the bottom')
            token = str(input(f'\n[{datetime.today().month}/{datetime.today().day}/{datetime.today().year} - {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}] Enter the bot token > '))

            if '"' in token:
                token = token.strip('"')
            elif "'" in token:
                token = token.strip("'")

            bot = {
                "huromi": {
                    "token": token
                },
                "status": [
                    "im away",
                    "sleeping",
                    "summer",
                    "{prefix} for help"
                ]
            }

            with open('bot.json', 'w') as f:
                json.dump(bot, f, indent=4)

            with open('bot.json') as f:
                settings = json.load(f)

            console.clear()
            return settings['huromi']['token']

    def prefix(self, bot, message):
        path = 'bot/db'
        
        if not os.path.exists(path):
            os.mkdir(path)
        try:
            with open(f'bot/db/{message.guild.id}.json') as f:
                data = json.load(f)
            return data['server']['prefix']
        except FileNotFoundError:
            with open(f'bot/db/{message.guild.id}.json', 'w') as f:
                json.dump(config_db, f, indent=4)
            with open(f'bot/db/{message.guild.id}.json') as f:
                data = json.load(f)
            return data['server']['prefix']