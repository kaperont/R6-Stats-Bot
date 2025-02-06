import logging
from json import JSONDecodeError

import discord
import requests
from bs4 import BeautifulSoup

from ..settings import settings

logger = logging.getLogger(__name__)


class R6TrackerService:
    BASE_HTML_URL = settings.BASE_TRACKER_HTML_URL
    BASE_API_URL = settings.BASE_TRACKER_API_URL
    DEFAULT_REQUEST_SETTINGS = settings.REQUEST_SETTINGS
    
    @classmethod
    def get_user_stats(cls, username: str, playlist: str = 'standard', platform: str = 'ubi'):
        try:
            url = f'{cls.BASE_API_URL}/{playlist}/profile/{platform}/{username}/'
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'TRN-Api-Key': settings.TRACKER_API_TOKEN
            }

            logger.info(f'Requesting stats for {username} on {playlist} playlist.')
            logger.info(f'Requesting from URL: "{url}"')

            response = requests.get(url, headers=headers, **cls.DEFAULT_REQUEST_SETTINGS)

            if not response.ok:
                logger.warning(f'Did not retrieve requested resource.  Reason: Received "{response.status_code}: {response.reason}"')

                return

            return response.json()

        except requests.RequestException as e:
            logger.error(f'Did not retrieve requested stats.  Reason: Encountered a Request Error.  Error: {e}')
            logger.debug('Traceback: ', exc_info=e)

            return
        
        except JSONDecodeError as e:
            logger.error(f'Did not process requested resource.  Reason: Could not JSON decode response data.  Error: {e}')
            logger.debug('Traceback: ', exc_info=e)

            return


    @classmethod
    def get_user_stats_from_html(cls, username: str, platform: str = 'ubi'):
        default_embed = discord.Embed(
            title='Could Not Track!',
            description=f'I could not track {username} on the specified platform ({platform}).',
            color=discord.Colour.red()
        )
        default_embed.set_author(name='R6 Tracker', icon_url='https://imgsvc.trackercdn.com/url/max-width(48),quality(66)/https%3A%2F%2Ftrackercdn.com%2Fcdn%2Ftracker.gg%2Fr6siege%2Fr6-ow-badge.png/image.png')
        default_embed.set_footer(text='Stats provided by TRN.', icon_url='https://trackercdn.com/static-files/trackergg/production/dist/client/assets/DSvub3La.png')
        default_embed.set_thumbnail(url='https://staticctf.ubisoft.com/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4sR4Qd4YtPGs6CyYUkVkFM/6ca0a342d790345d2ca23db3a6dfd69c/r6s-logo-ww.png')

        try:
            url = f'{cls.BASE_HTML_URL}/{platform}/{username}/overview'

            logger.info(f'Requesting stats for {username} from {url}.')

            response = requests.get(url, **cls.DEFAULT_REQUEST_SETTINGS)

            if not response.ok:
                logger.warning(f'Did not retrieve requested resource.  Reason: Received "{response.status_code}: {response.reason}"')

                return default_embed

            soup = BeautifulSoup(response.content)
            season_card = soup.find('div', class_='season-card')
            color_div = season_card.find('span', class_='text-secondary').find('span', class_='truncate')

            stats = season_card.header.get_text(separator='::').split('::')
            rank_img_url = season_card.find('img', class_='rank-image')['src']
            color = int(color_div['style'].strip('color:#').strip(';'), 16)
            # rgb = soup.find('div', class_='season-card').find('span', class_='text-secondary').find('span', class_='truncate')['style'].strip('color: rgb()').split(',')
            # color = discord.Color.from_rgb(*rgb)

            embed = discord.Embed(
                title=f'{stats[0]}  -  {stats[1]}',
                description=f'Here\'s what I found for {username}!',
                url=url,
                color=color
            )

            rp = f'`{stats[1]} RP`'
            rp += f' (*{stats[-1]}*)' if '%' in stats[-1] else ''

            embed.set_image(url=rank_img_url)
            embed.set_author(name='R6 Tracker', icon_url='https://imgsvc.trackercdn.com/url/max-width(48),quality(66)/https%3A%2F%2Ftrackercdn.com%2Fcdn%2Ftracker.gg%2Fr6siege%2Fr6-ow-badge.png/image.png')
            embed.add_field(name='Rank Points', value=rp)
            embed.set_footer(text='Stats provided by TRN.', icon_url='https://trackercdn.com/static-files/trackergg/production/dist/client/assets/DSvub3La.png')
            embed.set_thumbnail(url='https://staticctf.ubisoft.com/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4sR4Qd4YtPGs6CyYUkVkFM/6ca0a342d790345d2ca23db3a6dfd69c/r6s-logo-ww.png')

            return embed

        except requests.RequestException as e:
            logger.error(f'Did not retrieve requested stats.  Reason: Encountered a Request Error.  Error: {e}')
            logger.debug('Traceback: ', exc_info=e)

            return default_embed
