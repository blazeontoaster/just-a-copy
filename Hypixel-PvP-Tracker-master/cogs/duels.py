import hypixel
import discord
import json
import pymongo
from utils.duels import getDivisionTitle, getOverallTitle
from discord.ext import commands

cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']['colors']

class Duels(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.cooldown(1, 6, commands.BucketType.user)
	async def duels(self, ctx, playerName, game=None):
		color_db = db.find_one({"_id":ctx.author.id})
		if color_db is None:
			color = 0
		else:
			color = color_db['color']

		playerData = hypixel.Player(playerName).JSON
		duelsData = hypixel.Player(playerName).JSON['stats']['Duels']
		print(duelsData)
		if not game:
			embed = discord.Embed(title=f"{playerData['displayname']}'s Duels Stats", color=color)
			embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playerData['uuid']}?overlay")
			embed.set_author(name=f"Overall Duels Title - {await getOverallTitle(duelsData['wins'])}")
			embed.add_field(name="Coins", value=f"`{duelsData['coins']:,}`")
			embed.add_field(name="Games Played", value=f"`{duelsData['games_played_duels']:,}`")
			embed.add_field(name="Current Winstreak", value=f"`{duelsData['current_winstreak']:,}`")
			embed.add_field(name="Wins", value=f"`{duelsData['wins']:,}`")
			embed.add_field(name="Losses", value=f"`{duelsData['losses']:,}`")
			embed.add_field(name="WLR", value=f"`{round(duelsData['wins']/duelsData['losses'], 2)}`")
			embed.add_field(name="Kills", value=f"`{duelsData['kills']:,}`")
			embed.add_field(name="Deaths", value=f"`{duelsData['deaths']:,}`")
			embed.add_field(name="KDR", value=f"`{round(duelsData['kills']/duelsData['deaths'], 2)}`")
			await ctx.send(embed=embed)
		elif game.lower() == "bridge":
			embed = discord.Embed(title=f"{playerData['displayname']}'s Bridge Duels Stats", color=color)
			embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playerData['uuid']}?overlay")
			embed.set_author(name=f"Bridge Duels Title - The Bridge {await getDivisionTitle(playerData['achievements']['duels_bridge_wins'])}")
			embed.add_field(name="Overall:", value=f"""- **Best WS**: `{duelsData['best_bridge_winstreak']:,}`
			- **Current WS**: `{duelsData['current_bridge_winstreak']:,}`
			- **Wins**: `{playerData['achievements']['duels_bridge_wins']:,}`
			- **Losses**: `{duelsData['bridge_duel_rounds_played']-playerData['achievements']['duels_bridge_wins']:,}`""")
			await ctx.send(embed=embed)
		

def setup(bot):
	bot.add_cog(Duels(bot))