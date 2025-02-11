import logging

import discord
from discord.ext import commands

from ..models import User

logger = logging.getLogger(__name__)


class MongoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='claim', description='Claims a particular R6 Siege account.')
    async def claim(self, ctx):
        if (await User.find_one(User.user_id == ctx.author.id)) is None:
            await ctx.respond(view=PlatformSelectView(), ephemeral=True)
            return

        await ctx.respond(view=ConfirmUserOverwriteView(), ephemeral=True)


    @discord.slash_command(name='user', description='Displays user data.')
    async def user(self, ctx):
        if (user := await User.find_one(User.user_id == ctx.author.id)) is None:
            embed = discord.Embed(
                title='No Account Claimed',
                description='You have not yet claimed an account! To claim an R6 Account, use `/claim`.',
                color=discord.Colour.red()
            )

            await ctx.respond(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(title='Located Account!', color=discord.Colour.green())
        embed.add_field(name="Handle", value=ctx.author.mention)
        embed.add_field(name="Username", value=f'`{user.username}`')
        embed.add_field(name="Platform", value=f'`{user.platform}`')

        await ctx.respond(embed=embed)


class UserModal(discord.ui.Modal):
    def __init__(self, platform: str = 'ubi', is_update: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.platform = platform
        self.is_update = is_update
        self.add_item(discord.ui.InputText(label='Username'))

    async def callback(self, interaction: discord.Interaction):
        user_data = {
            'user_id': interaction.user.id,
            'username': self.children[0].value,
            'platform': self.platform,
        }

        embed = discord.Embed(title='Account Claimed!', color=discord.Colour.green())
        embed.add_field(name="Handle", value=interaction.user.mention)
        embed.add_field(name="Username", value=f'`{self.children[0].value}`')
        embed.add_field(name="Platform", value=f'`{self.platform}`')

        if self.is_update:
            if (user := await User.find_one(User.user_id == interaction.user.id)) is None:
                logger.waring('Attempted to update user that does not exist.')
                return

            await user.set(user_data)

        else:
            user = User(**user_data)
            await user.save()

        await interaction.response.send_message(embeds=[embed])


class PlatformSelectView(discord.ui.View):
    PLATFORM_OPTIONS = [
        discord.components.SelectOption(label='Ubisoft', value='ubi'),
        discord.components.SelectOption(label='Xbox', value='xbl'),
        discord.components.SelectOption(label='PlayStation', value='psn'),
    ]
    
    def __init__(self, *items, timeout = 180, disable_on_timeout = False, **kwargs):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)

        self.is_update = kwargs.get('is_update', False)

    @discord.ui.select(placeholder='Select a Platform', options=PLATFORM_OPTIONS)
    async def platform_callback(self, select, interaction):
        modal = UserModal(title='Claim Account', is_update=self.is_update, platform=select.values[0])
        await interaction.response.send_modal(modal)
        self.stop()


class ConfirmUserOverwriteView(discord.ui.View):
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def reject_callback(self, button, interaction):
        await interaction.response.send_message('Canceled Action!', ephemeral=True)
        self.stop()

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.primary)
    async def confirm_callback(self, button, interaction):
        await interaction.response.send_message('Select a Platform', view=PlatformSelectView(is_update=True), ephemeral=True)
        self.stop()


def setup(bot: commands.Bot):
    bot.add_cog(MongoCog(bot))
