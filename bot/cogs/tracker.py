import logging

import discord
from discord.ext import commands

from ..services import R6TrackerService

logger = logging.getLogger(__name__)


class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def hello(self, ctx: commands.Context, *, member: discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.mention}!')

        else:
            await ctx.send(f'Hello {member.mention}... This feels familiar.')

        self._last_member = member

    @discord.user_command()
    async def greet(self, ctx, member: discord.Member):
        await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}!')

    @discord.slash_command(name='track', description = 'Track the specified user\'s stats.')
    async def track(self, ctx, username: str, playlist: discord.Option(str, choices=['standard', 'ranked'], default='standard'), platform: discord.Option(str, choices=['ubi', 'xbl', 'psn'], default='ubi')):
        data = R6TrackerService.get_user_stats(username, playlist, platform)

        logger.debug(f'User Data: {data}')
        await ctx.respond('Got the data! Or did I... Tracking is coming soon!')
    
    @discord.slash_command(name='rank', description='The rank of the specified user.')
    async def rank(self, ctx, username: str, platform: discord.Option(str, choices=['ubi', 'xbl', 'psn'], default='ubi')):
        embed = R6TrackerService.get_user_stats_from_html(username, platform)

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Tracker(bot))
