import discord
from discord.ext import commands
import requests
import hypixel
from datetime import datetime
import pymongo

class HypixelGuild(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def guild(self, ctx, guild):
		cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
		db = cluster['data']
		color_db = db['colors']

		color = color_db.find_one({"_id": ctx.author.id})

		if color is None:
			colors = 0
		else:
			colors = color['color']
		
		data = requests.get(f'https://api.hypixel.net/guild?key=20935b96-fb6f-434d-a28a-e28abee6af8f&name={guild}').json()

		guild_member_list = []

		for x in data['guild']['members']:
			player_name = hypixel.Player(x['uuid']).JSON['displayname']
			guild_member_list.append(f"{discord.utils.escape_markdown(player_name)} - {datetime.strftime(datetime.fromtimestamp(x['joined']/1000), '%Y-%m-%d')}")
		
		embed = discord.Embed(color=colors)
		embed.add_field(name="Member List", value=str('\n'.join(guild_member_list))[0:1023])
		embed.add_field(name="Created At", value=datetime.strftime(datetime.fromtimestamp(data['guild']['created']/1000), '%A, %B %-d, %Y at %-I:%M %p UTC'))

		await ctx.send(embed=embed)
		

def setup(bot):
	bot.add_cog(HypixelGuild(bot))