import logging
from json import JSONDecodeError

import requests

from ..settings import settings

logger = logging.getLogger(__name__)

REQUEST_SETTINGS = settings.REQUEST_SETTINGS.to_dict()
REQUEST_SETTINGS['cert'] = tuple(REQUEST_SETTINGS.get('cert', []))


class R6TrackerService:
    base_url = settings.BASE_TRACKER_API_URL
    DEFAULT_REQUEST_SETTINGS = REQUEST_SETTINGS
    
    @classmethod
    def get_user_stats(cls, username: str, playlist: str = 'standard'):
        try:
            url = f'{cls.base_url}/{playlist}/profile/ubi/{username}/'

            logger.info(f'Requesting stats for {username} on {playlist} playlist.')
            logger.info(f'Requesting from URL: "{url}"')

            response = requests.get(url, **cls.DEFAULT_REQUEST_SETTINGS)

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
