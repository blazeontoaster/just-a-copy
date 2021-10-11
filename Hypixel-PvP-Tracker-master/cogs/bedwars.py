import discord
import os
import hypixel
from discord.ext import commands
import pymongo

cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
color_db = db['colors']

class BedWars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    hypixel.setKeys([os.environ.get('HYPIXEL_KEY')])

    @commands.command(aliases=['bw'])
    @commands.cooldown(1, 3, commands.BucketType.user)	
    async def bedwars(self, ctx, player):
        colors = color_db.find_one({"_id":ctx.author.id})
        if colors is None:
            color = 0
        else:
            color = colors['color']
        try: 
            user = hypixel.Player(player).JSON
            print(user)
            displayName = user['displayname']
            bedwars = user['stats']['Bedwars']
            gamesPlayed = bedwars['games_played_bedwars_1']
            deaths = bedwars['deaths_bedwars']
            bedsLost = bedwars['beds_lost_bedwars']
            kills = bedwars["kills_bedwars"]
            winstreak = bedwars["winstreak"]
            bedsBroken = bedwars["beds_broken_bedwars"]
            wins = bedwars['wins_bedwars']
            finalDeaths = bedwars['final_deaths_bedwars']
            finalKills = bedwars['final_kills_bedwars']
            gamesLost = gamesPlayed-wins
            embed=discord.Embed(title=f'{displayName}\'s BedWars Stats', color=discord.Color(color))
            kdr = kills/deaths
            kdr_rounded = round(kdr, 2)
            fkdr = round((finalKills/finalDeaths), 2)
            embed.add_field(name="Total Games Played", value=gamesPlayed)
            embed.add_field(name="Kills", value=kills)
            embed.add_field(name="Wins/Losses", value=f'{wins}-{gamesLost}')
            embed.add_field(name="Winstreak", value=winstreak)
            embed.add_field(name="Beds Broken", value=bedsBroken)
            embed.add_field(name="Deaths", value=deaths)
            embed.add_field(name="Beds Lost", value=bedsLost)
            embed.add_field(name="KDR (Kill Death Ratio)", value=kdr_rounded)
            embed.add_field(name="FKDR (Final Kill Death Ratio)", value=fkdr)
            embed.set_thumbnail(url=f'https://minotar.net/avatar/{player}/200')
            await ctx.send(embed=embed)
        except hypixel.PlayerNotFoundException:
            e2 = discord.Embed(title=':x: Player Not Found', description=f"{ctx.author.mention}, {player} was nowhere to be found :O", color=0xff0000)
            await ctx.send(embed=e2)
        
        except KeyError:
            e2 = discord.Embed(title=':x: Hypixel Error', description=f"{ctx.author.mention}, there was an error. Either {player} has not played BedWars before, or something is wrong with the Hypixel API.", color=0xff0000)
            await ctx.send(embed=e2)  

def setup(bot):
    bot.add_cog(BedWars(bot))