import discord
import asyncio
import json
from bot import bot_core
from typing import Union
from discord.ext import commands
core = bot_core()

class guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def changesettings(self, ctx):
        embed_color = core.return_embed_color(id=ctx.guild.id)
        language = core.get_language(id=ctx.guild.id, category='hug')

        embed = discord.Embed(
            title = f'Change settings!',
            color = embed_color,
            description='1️⃣ - Set langauge or change [Spanish/English]\n2️⃣ - '
        )
        embed.set_footer(text='> Request by {}'.format(ctx.author), icon_url=ctx.author.avatar.url)
        text = await ctx.send(embed=embed)

        await text.add_reaction("1️⃣")
        await text.add_reaction("2️⃣")
        await text.add_reaction("3️⃣")
        await text.add_reaction("4️⃣")
        await text.add_reaction("5️⃣")

        def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and \
               str(r.emoji) in ["1️⃣", "2️⃣", "3️⃣", '4️⃣', "5️⃣"]
        
        def check_lan(r: discord.Reaction, u: Union[discord.Member, discord.User]):
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and \
               str(r.emoji) in ["1️⃣", "2️⃣"]

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check = check, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"**{ctx.author}**, you didnt react with a ✅ or ❌ in 60 seconds.")
            return
        else:
            if str(reaction.emoji) == "1️⃣":
                embed = discord.Embed(
                    color = embed_color,
                    description = 'Please select your language!\n\n1️⃣ - Spanish\n2️⃣ - English'
                )
                lan = await ctx.send(embed=embed)
                await lan.add_reaction("1️⃣")
                await lan.add_reaction("2️⃣")

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check = check_lan, timeout = 60.0)
                except:
                    return await ctx.send('Timeout')
                else:
                    with open('bot/db/{}.json'.format(ctx.guild.id)) as f:
                        lan_change = json.load(f)
                    
                    if str(reaction.emoji) == "1️⃣":
                        language = 'spanish'
                        msg = 'Lenguaje a sido cambido a Español (Mexico)'
                    else:
                        language = 'english'
                        msg = 'Language changed to English (Native)'

                    d2 = discord.Embed(
                        color = embed_color,
                        description = msg
                    )
                    
                    lan_change['server']['language'] == language

                    with open('bot/db/{}.json'.format(ctx.guild.id), 'w') as f:
                        json.dump(lan_change, f, indent=4)
                    
                    await lan.edit(embed=d2, delete_after=3)
                
            if str(reaction.emoji) == ":two:":
                return await ctx.send(f":(")

async def setup(bot):
    await bot.add_cog(guild(bot=bot))