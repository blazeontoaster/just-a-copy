from discord.ext import commands
import pymongo
import discord

cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
color_db = db['colors']

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def support_server(self, ctx):
        await ctx.send('My support server:\nhttps://discord.gg/bbcHY6YNmw')
    
    @commands.command()
    async def invite(self, ctx):
        await ctx.send('My Invite Link (all perms needed):\nhttps://discord.com/oauth2/authorize?client_id=770742451882164234&permissions=387136&scope=bot')
    
    @commands.command()
    async def vote(self, ctx):
        colors = color_db.find_one({"_id": ctx.author.id})
        if colors is None:
            color = 0
        else:
            color = colors['color']
        embed=discord.Embed(title="Vote for me!", color = discord.Color(color))
        embed.description = """[top.gg](https://top.gg/bot/770742451882164234/vote)
[Discord Bots](https://discord.bots.gg/bots/770742451882164234/)
[Bots For Discord](https://botsfordiscord.com/bot/770742451882164234)
"""
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Support(bot))