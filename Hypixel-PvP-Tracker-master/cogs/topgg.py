from discord.ext import commands

import dbl


class TopGG(commands.Cog):
    """
    This example uses dblpy's autopost feature to post guild count to top.gg every 30 minutes.
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc3MDc0MjQ1MTg4MjE2NDIzNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA3MjczNzEwfQ.7GDJyQvR-T_RNRMzoYDQjpRQv7CvEGTVqMTAGF7cO1g'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)  # Autopost will post your guild count every 30 minutes

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")


def setup(bot):
    bot.add_cog(TopGG(bot))