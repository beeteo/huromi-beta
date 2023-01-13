import discord, json
from bot import bot_core
from Consolly import consoler
from discord.ext import commands

console = consoler()
core = bot_core()
bot = commands.Bot(command_prefix=(core.prefix), intents=discord.Intents.all())

@bot.event
async def on_connect():
    console.set_title(f'Huromi : Status: Connected! : {bot.user.name}')
    await core.cogload(bot=bot)
    await core.anim_presence(bot=bot)

if __name__ == '__main__':
    bot.run(core.get_token())