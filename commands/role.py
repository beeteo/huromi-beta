import discord
from bot import bot_core
from discord.ext import commands
core = bot_core()

class role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kiss(self, ctx, user: discord.Member=None):
        data = core.roleapi(category='kiss', type='gif')
        embed_color = core.return_embed_color(id=ctx.guild.id)
        language = core.get_language(id=ctx.guild.id, category='kiss')

        if user is None:
            return await ctx.send('Necesitas mencionar a alguien para usar este comando!')
        else:
            embed = discord.Embed(
                color = embed_color,
                description = f'{language}'.replace('{user.mention}', user.mention).replace('{author.mention}', ctx.author.mention)
            )
            embed.set_image(url=data[0])
            embed.set_footer(text=data[1])
            await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, user: discord.Member=None):
        data = core.roleapi(category='hug', type='gif')
        embed_color = core.return_embed_color(id=ctx.guild.id)
        language = core.get_language(id=ctx.guild.id, category='hug')
        print(language)

        if user is None:
            return await ctx.send('Necesitas mencionar a alguien para usar este comando!')
        else:
            embed = discord.Embed(
                color = embed_color,
                description = f'{language}'.replace('{user.mention}', user.mention).replace('{author.mention}', ctx.author.mention)
            )
            embed.set_image(url=data[0])
            embed.set_footer(text=data[1])
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(role(bot))