import discord
import json
from discord.ext import commands
import pymongo

cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
prefixes = db['prefixes']


class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Hypixel With {len(self.bot.guilds)} Servers | ./help"))
        prefixes.insert_one({"_id": guild.id, "prefix": "./"})
        channel = self.bot.get_channel(777971027711229991)
        bots = 0
        for x in guild.members:
            if x.bot:
                bots+=1
        members = guild.member_count-bots
        await channel.send(f"""
Joined **{guild.name}**!
Member Count: **{guild.member_count}**
Owner: **{guild.owner}**
ID: **{guild.id}**
Bots: **{bots}**
Humans: **{members}**""")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Hypixel With {len(self.bot.guilds)} Servers | ./help"))
        prefixes.delete_one({"_id": guild.id})
        channel = self.bot.get_channel(777971027711229992)
        bots = 0
        for x in guild.members:
            if x.bot:
                bots+=1
        members = guild.member_count-bots
        await channel.send(f"""
Left **{guild.name}**!
Member Count: **{guild.member_count}**
Owner: **{guild.owner}**
ID: **{guild.id}**
Bots: **{bots}**
Humans: **{members}**""")

def setup(bot):
    bot.add_cog(Guild(bot))