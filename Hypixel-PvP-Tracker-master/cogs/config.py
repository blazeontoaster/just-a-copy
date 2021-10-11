from discord.ext import commands
import random
import discord
import json
import requests
import pymongo


cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
color_db = db['colors']
prefix_db = db['prefixes']

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['c'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def set_color(self, ctx, hex_code):
        if len(hex_code) > 6:
            await ctx.send('The hex code provided is invalid.')
            return
        try:
            api = requests.get(f'https://www.thecolorapi.com/id?format=json&hex={hex_code}').json()
            color = requests.get(f"https://www.colourlovers.com/api/color/{hex_code}?format=json").json()
            name = api['name']['value']
            hex_code = int(f'0x{hex_code}', 0)
            e1 = discord.Embed(color=hex_code, title=name)
            e1.set_author(name="This is the color that you are setting it to.")
            e1.add_field(name="Hex Value", value=discord.Color(hex_code))
            e1.add_field(name="RGB Value", value=str(discord.Color(hex_code).to_rgb())[1:-1])
            e1.set_thumbnail(url=color[0]["imageUrl"])
        except:
            api = requests.get(f'https://www.thecolorapi.com/id?format=json&hex={hex_code}').json()
            color = requests.get(f"https://www.colourlovers.com/api/color/{hex_code}?format=json").json()
            name = api['name']['value']
            hex_code = int(f'0x{hex_code}', 0)
            e1 = discord.Embed(color=hex_code, title=name)
            e1.set_author(name="This is the color that you are setting it to.")
            e1.add_field(name="Hex Value", value=discord.Color(hex_code))
            e1.add_field(name="RGB Value", value=str(discord.Color(hex_code).to_rgb())[1:-1])
        await ctx.send(embed=e1)

        color_db.update_one({"_id": ctx.author.id}, {"$set": {"color": hex_code}})
    
    @commands.command(aliases=['p'])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def set_prefix(self, ctx, prefix):     
        if prefix == "<@!770742451882164234>":
            await ctx.send(':x: Not a valid prefix.')
        else:
            await ctx.send(f":white_check_mark: The prefix for this server is now **{prefix}**.")
            prefix_db.update_one({"_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
    
def setup(bot):
    bot.add_cog(Config(bot))