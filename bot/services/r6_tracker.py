import logging
from json import JSONDecodeError

import requests

from ..settings import settings

logger = logging.getLogger(__name__)


class R6TrackerService:
    def __init__(self):
        self.base_url = settings.BASE_TRACKER_API_URL
    
    def get_user_stats(self, username: str, playlist: str = 'standard'):
        try:
            url = f'{self.base_url}/standard/profile/ubi/{username}/stats/overview/rankPoints/'

            logger.info(f'Requesting stats for {username} on {playlist} playlist.')
            logger.info(f'Requesting from URL: "{url}"')

            response = requests.get(url)

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
