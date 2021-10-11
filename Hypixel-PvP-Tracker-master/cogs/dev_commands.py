import discord
from discord.ext import commands
import pymongo
from datetime import datetime

cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
colorDB = db['colors']

def is_it_me(ctx):
    return ctx.author.id == 475315771086602241

class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    
    @commands.command()
    @commands.check(is_it_me)
    async def all_guilds(self, ctx):
        for x in self.bot.guilds:
            bots = 0
            for i in x.members:
                if i.bot:
                    bots+=1
            guild_created_at = datetime.strftime(x.created_at, "%A, %B %d, %Y")
            embed=discord.Embed()
            embed.description = (f"**Name**: {x.name}\n**ID**: {x.id}\n**Humans**: {len(x.members)-bots}\n**Bots**: {bots}\n**Created At**: {guild_created_at}\n**Owner**: {x.owner}")
            embed.set_thumbnail(url=x.icon_url)
            await ctx.send(embed=embed)   
        await ctx.send(f'{len(self.bot.guilds)} guilds!')



    
def setup(bot):
    bot.add_cog(DevCommands(bot))