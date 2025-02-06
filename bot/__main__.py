import logging

import discord
from beanie import init_beanie
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

from .models import User
from .settings import settings

logger = logging.getLogger(__name__)

class Bot(commands.Bot):

    async def on_ready(self):
        await self.setup_mongo()

        logger.info(f'Logged on as {self.user.name}')

    async def setup_mongo(self):
        client = AsyncIOMotorClient(
            settings.DB_URL
        )

        await init_beanie(database=client[settings.DATABASE_NAME], document_models=[User])


def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot(command_prefix='!', intents=intents)
    bot.load_extension('bot.cogs.tracker')
    bot.load_extension('bot.cogs.mongo')

    bot.run(settings.DISCORD_BOT_TOKEN)


if __name__ == '__main__':
    main()
