import os
import gevent.monkey
gevent.monkey.patch_all()
import discord
import pymongo
import asyncio
from discord.ext import commands



cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
prefix_db = db['prefixes']
color_db = db['colors']

def get_prefix(bot, message):    
	if message.guild is None:
		return ''
	else:
		prefix = prefix_db.find_one({"_id": message.guild.id})
		return prefix['prefix']

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Hypixel with {len(bot.guilds)} Servers | Tag For Prefix"))
	print(f"""Logged in as {bot.user}
User ID: {bot.user.id}
--------------------------------
discord.py version: {discord.__version__}
bot is in {len(bot.guilds)} servers"""
	)




def is_it_me(ctx):
	return ctx.author.id == 475315771086602241


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
@commands.check(is_it_me)
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}')
	await ctx.send(f':white_check_mark: Successfully loaded **{extension}**!')


@bot.command()
@commands.check(is_it_me)
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
	await ctx.send(f':white_check_mark: Successfully unloaded **{extension}**!')


@bot.command()
@commands.check(is_it_me)
async def reload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
	bot.load_extension(f'cogs.{extension}')
	await ctx.send(f':white_check_mark: Successfully reloaded **{extension}**!')    

@bot.event  
async def on_command(ctx):
	color = color_db.find_one({"_id": ctx.author.id})
	if color is None:
		color_db.insert_one({"_id": ctx.author.id, "color":0})
	
	
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		embed = discord.Embed(title=":x: Cooldown", description=f"{ctx.author.mention}, you are on cooldown. Try again in **{round(error.retry_after)} seconds**.", color=0xff0000)
		await ctx.send(embed=embed)
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(title=":x: Missing Argument", description=f"{ctx.author.mention}, you are missing a required argument.", color=0xff0000)
		await ctx.send(embed=embed)
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title=":x: Missing Permissions", description=f"{ctx.author.mention}, {str(error)}", color=0xff0000)
		await ctx.send(embed=embed)
	raise error

@bot.event
async def on_message(message):
	if message.content == "<@!770742451882164234>":
		prefix = prefix_db.find_one({"_id": message.guild.id})
		await message.channel.send(f"My prefix for this guild is **{prefix['prefix']}**")
	
	await bot.process_commands(message)

	
bot.run(os.environ.get('BOT_TOKEN'))
