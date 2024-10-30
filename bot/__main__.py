import logging

import discord
from discord.ext import commands

from .settings import settings

logger = logging.getLogger(__name__)

class Bot(commands.Bot):

    async def on_ready(self):
        logger.info(f'Logged on as {self.user.name}')

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot(command_prefix='!', intents=intents)
    bot.load_extension('bot.cogs.tracker')
    bot.load_extension('bot.cogs.mongo')

    bot.run(settings.DISCORD_BOT_TOKEN)


if __name__ == '__main__':
    main()
