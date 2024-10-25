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
    async def hello(self, ctx: commands.context.Context, *, member: discord.Member = None):
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
    async def track(self, interaction: discord.Interaction, username: str, playlist: str = 'standard'):
        data = R6TrackerService.get_user_stats(username, playlist)

        logger.debug(f'User Data: {data}')
        await interaction.response.send_message('Got the data! Or did I... Tracking is coming soon!')


def setup(bot: commands.Bot):
    bot.add_cog(Tracker(bot))
