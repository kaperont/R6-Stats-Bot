import logging

import discord
from discord.ext import commands

from ..services import MongoDBService, R6TrackerService

logger = logging.getLogger(__name__)


class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = MongoDBService()

    @discord.slash_command(name='rank', description='The rank of the specified user.')
    async def rank(self, ctx, platform: discord.Option(str, choices=['ubi', 'xbl', 'psn'], default='ubi'), username: str | None = None):
        if username:
            embed = R6TrackerService.get_user_stats_from_html(username, platform)
            await ctx.respond(embed=embed)

            return

        try:
            user = self.service.get(user_id=ctx.author.id)
            embed = R6TrackerService.get_user_stats_from_html(user['username'], user['platform'])

        except self.service.DoesNotExist:
            await ctx.respond(embed=discord.Embed(
                title='No Account Claimed!',
                description='Please claim an R6 Account using `/claim`, or provide a `username` to track.',
                color=discord.Colour.red()
            ), ephemeral=True)
            return

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Tracker(bot))
