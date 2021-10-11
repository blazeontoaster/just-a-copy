import discord
import asyncio
from discord.ext import commands
import pymongo

cluster = pymongo.MongoClient('mongodb+srv://PvP_Bot:HypixelPog@hypixel-pvp-tracker.q7y1y.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['data']
color_db = db['colors']
prefix_db = db['prefixes']

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
       
        if ctx.guild is None:
            await ctx.send(':x: This command cannot be used in a DM Channel!')
            return
        
        prefixes = prefix_db.find_one({"_id": ctx.guild.id})
        prefix = prefixes['prefix']
        
        color = color_db.find_one({"_id": ctx.author.id})

        if color is None:
            colors = 0
        else:
            colors = color['color']
        if ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            stats_embed = discord.Embed(title="Stat Commands", color=colors)
            stats_embed.add_field(name="BedWars Stats", value=f"`{prefix}bedwars <player>`", inline=False)
            stats_embed.add_field(name="SkyWars Stats", value=f"`{prefix}skywars <player>`", inline=False)
            stats_embed.add_field(name="Bridge Duel Stats", value=f"`{prefix}bridge <player>`", inline=False)
            stats_embed.set_footer(text=f"{ctx.author.name} • Page 1/4", icon_url=ctx.author.avatar_url)
            config_embed = discord.Embed(title="Config Commands", color=colors)
            config_embed.add_field(name="Set Embed Color", value=f"`{prefix}set_color <hex_code>`", inline=False)
            config_embed.add_field(name="Change Server Prefix", value=f"`{prefix}set_prefix <prefix>`", inline=False)
            config_embed.set_footer(text=f"{ctx.author.name} • Page 2/4", icon_url=ctx.author.avatar_url)
            support_embed = discord.Embed(title="Support Commands", color=colors)
            support_embed.add_field(name="Support Server", value=f"`{prefix}support_server`", inline=False)
            support_embed.add_field(name="Invite Link", value=f"`{prefix}invite`", inline=False)
            support_embed.add_field(name="Vote On Botlists", value=f"`{prefix}vote`", inline=False)
            support_embed.set_footer(text=f"{ctx.author.name} • Page 3/4", icon_url=ctx.author.avatar_url)
            other_embed = discord.Embed(title="Other Commands", color=colors)
            other_embed.add_field(name="Get A Hypixel User's Profile", value=f"`{prefix}profile <player>`", inline=False)
            other_embed.set_footer(text=f"{ctx.author.name} • Page 4/4", icon_url=ctx.author.avatar_url)
            contents = [stats_embed, config_embed, support_embed, other_embed]
            pages = len(contents)
            cur_page = 1
            message = await ctx.send(embed=contents[cur_page-1])

            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        await message.edit(embed=contents[cur_page-1])
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        await message.edit(embed=contents[cur_page-1])
                        await message.remove_reaction(reaction, user)

                    else:
                        await message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    break
        
        else:
            embed = discord.Embed(title="Hypixel PvP Tracker Commands", color=discord.Color(colors))
            embed.add_field(name="BedWars Stats", value=f"`{prefix}bedwars <player>`", inline=False)
            embed.add_field(name="SkyWars Stats", value=f"`{prefix}skywars <player>`", inline=False)
            embed.add_field(name="SkyWars Stats", value=f"`{prefix}skywars <player>`", inline=False)
            embed.add_field(name="Bridge Duel Stats", value=f"`{prefix}bridge <player>`", inline=False)
            embed.add_field(name="Set Embed Color", value=f"`{prefix}set_color <hex_code>`", inline=False)
            embed.add_field(name="Change Server Prefix", value=f"`{prefix}set_prefix <prefix>`", inline=False)
            embed.add_field(name="Support Server", value=f"`{prefix}support_server`", inline=False)
            embed.add_field(name="Invite Link", value=f"`{prefix}invite`", inline=False)
            embed.add_field(name="Vote On Botlists", value=f"`{prefix}bote`", inline=False)
            embed.add_field(name="Get A User's Hypixel Profile", value=f"`{prefix}profile <player>`", inline=False)
            await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(HelpCommand(bot))