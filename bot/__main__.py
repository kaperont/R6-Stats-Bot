import logging

import discord
from discord.ext import commands

from .services import R6TrackerService
from .settings import settings

logger = logging.getLogger(__name__)

guild = discord.Object(id=settings.DISCORD_GUILD_ID)
GUILD_ID = discord.Object(id=settings.DISCORD_GUILD_ID)


class Client(commands.Bot):
    
    async def on_ready(self):
        logger.info(f'Logged on as {self.user}')
        try:
            synced = await self.tree.sync(guild=guild)
            logger.info(f'Synced {len(synced)} commands to guild { guild.id}')
        except Exception as e:
            logger.debug(e)


if __name__ == '__main__':
    service = R6TrackerService()

    intents = discord.Intents.default()
    intents.message_content = True

    client = Client(command_prefix='!', intents=intents)

    @client.tree.command(name='r6-ping', description = 'Ping Pong', guild=GUILD_ID)
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message('pong')
    
    @client.tree.command(name='trackme', description = 'Track Me', guild=GUILD_ID)
    async def track_me(interaction: discord.Interaction, username: str, playlist: str = 'standard'):
        data = service.get_user_stats(username, playlist)

        logger.debug(data)
        await interaction.response.send_message('Got the data!')

    client.run(settings.DISCORD_BOT_TOKEN)
