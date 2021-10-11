import discord
import hypixel
from datetime import datetime
from discord.ext import commands
import pymongo

cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
color_db = db['colors']
prefix_db = db['prefixes']

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self, ctx, user):
        colors = color_db.find_one({"_id": ctx.author.id})
        if colors is None:
            color = 0
        else:
            color = colors['color']
        try:
            player = hypixel.Player(user).JSON
            aliases = player['knownAliases']
            aliasesProper = ', '.join(aliases)
            name = player['displayname']
            socialLinks = []
            try:
                socialMedia = list(player['socialMedia']['links'])[0:len(player['socialMedia']['links'])]
                for x in socialMedia:
                    socialLinks.append(player['socialMedia']['links'][x])
            except:
                socialLinks.append('None')
            print(socialLinks)
            if socialLinks[0] == 'None':
                socialLinks = ''.join(socialLinks)
            else:
                socialLinks = '\n'.join(socialLinks)
            firstLogin = datetime.fromtimestamp(player['firstLogin']/1000)
            firstLoginProper = datetime.strftime(firstLogin, '%A, %B %-d, %Y at %-I:%M %p UTC')
            recentLogin = datetime.fromtimestamp(player['lastLogin']/1000)
            recentLoginProper = datetime.strftime(recentLogin, '%A, %B %-d, %Y at %-I:%M %p UTC')
            uuid = player['uuid']
            embed = discord.Embed(title=f"{name}'s Hypixel Profile", color=discord.Color(color))
            embed.add_field(name="First Login", value=firstLoginProper)
            embed.add_field(name="Most Recent Login", value=recentLoginProper)
            embed.add_field(name="Old Usernames", value=aliasesProper)
            embed.add_field(name="UUID", value=uuid)
            embed.add_field(name="Social Media Links", value=socialLinks)
            await ctx.send(embed=embed)
        except hypixel.PlayerNotFoundException:
            e2 = discord.Embed(title=':x: Player Not Found', description=f"{ctx.author.mention}, {user} was nowhere to be found :O", color=0xff0000)
            await ctx.send(embed=e2)
    
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def botInfo(self, ctx):
        if ctx.guild is None:
            await ctx.send(':x: This command cannot be used in DM\'s.')
            return
        prefixes = prefix_db.find_one({"_id": ctx.guild.id})
        colors = color_db.find_one({"_id": ctx.author.id})
        embed = discord.Embed(title="Hypixel PvP Tracker Info", color=discord.Color(colors['color']))
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=len(self.bot.users))
        embed.add_field(name="Channels", value=str(len(set(self.bot.get_all_channels()))))  
        embed.add_field(name="Server Prefix", value=prefixes['prefix'])
        embed.add_field(name="Library", value=f"discord.py v{discord.__version__}")
        embed.add_field(name="Support Server", value=f"https://discord.gg/bbcHY6YNmw")
        embed.add_field(name="Bot Invite", value=f"[Bot Invite](https://discord.com/oauth2/authorize?client_id=770742451882164234&permissions=387136&scope=bot)")
        await ctx.send(embed=embed)


    
def setup(bot):
    bot.add_cog(Other(bot))