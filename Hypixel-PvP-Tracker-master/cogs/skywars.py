import discord
import hypixel
from discord.ext import commands
import pymongo

cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
color_db = db['colors']

class SkyWars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['sw'])
    @commands.cooldown(1, 3, commands.BucketType.user)	
    async def skywars(self, ctx, player):
        colors = color_db.find_one({"_id": ctx.author.id})
        if colors is None:
            color = 0
        else:
            color = colors['color']
        try:
            user = hypixel.Player(player).JSON
            displayName = user['displayname']
            skywars = user['stats']['SkyWars']
            gamesPlayed = skywars['games_played_skywars']
            chestsOpened = skywars['chests_opened']
            lastMode = skywars['lastMode']
            losses = skywars['losses']
            quits = skywars['quits']
            winStreak = skywars['win_streak']
            arrowsShot = skywars['arrows_shot']
            wins = gamesPlayed - losses
            embed=discord.Embed(title=f"{displayName}'s SkyWars Stats", color=discord.Color(color))
            embed.add_field(name="Total Games Played", value=gamesPlayed)
            embed.add_field(name="Chests Opened", value=chestsOpened)
            embed.add_field(name="Last Mode Played", value=lastMode)
            embed.add_field(name="Winstreak", value=winStreak)
            embed.add_field(name="Wins/Losses", value=f"{wins}-{losses}")
            embed.add_field(name="Quits", value=quits)
            embed.add_field(name="Arrows Shot", value=arrowsShot)
            embed.set_thumbnail(url=f'https://minotar.net/avatar/{player}/200')
            await ctx.send(embed=embed)
        except hypixel.PlayerNotFoundException:
            e2 = discord.Embed(title=':x: Player Not Found', description=f"{ctx.author.mention}, {player} was nowhere to be found :O", color=0xff0000)
            await ctx.send(embed=e2)
        
        except KeyError:
            e2 = discord.Embed(title=':x: Hypixel Error', description=f"{ctx.author.mention}, there was an error. Either {player} has not played SkyWars before, or something is wrong with the Hypixel API.", color=0xff0000)
            await ctx.send(embed=e2)  
        

def setup(bot):
    bot.add_cog(SkyWars(bot))