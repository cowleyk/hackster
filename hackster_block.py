from nio.properties import StringProperty, PropertyHolder, \
    ObjectProperty, VersionProperty
from nio.signal.base import Signal

from .rest_polling.rest_polling_base import RESTPolling
from .oauth2_mixin.oauth2_password import OAuth2PasswordGrant

HACKSTER_URL_BASE = 'http://api.hackster.io/v2/'


class HacksterCreds(PropertyHolder):
    client_id = StringProperty(title='Hackster App client ID',
                               default='[[HACKSTER_CLIENT_ID]]')
    client_secret = StringProperty(title='Hackster App client secret',
                                   default='[[HACKSTER_CLIENT_SECRET]]')


class Hackster(OAuth2PasswordGrant, RESTPolling):

    version = VersionProperty('0.1.0')
    creds = ObjectProperty(HacksterCreds, title='Hackster Credentials')
    endpoint = StringProperty(title='Hackster Endpoint to poll',
                              default='projects')

    def get_oauth_base_url(self):
        return 'https://www.hackster.io/oauth/'

    def _authenticate(self):
        try:
            token_info = self.get_access_token(
                grant_type='client_credentials',
                addl_params={
                    'client_id': self.creds().client_id(),
                    'client_secret': self.creds().client_secret()
                })
            self.logger.debug('Token retrieved: {}.'.format(token_info))
        except:
            self.logger.exception('Error obtaining access token')

    def _prepare_url(self, paging=False):
        self._url = '{}{}'.format(HACKSTER_URL_BASE, self.endpoint())

        if not self.authenticated():
            self.logger.error('You must be authenticated to poll')
            return

        try:
            return self.get_access_token_headers()
        except:
            self.logger.exception('Unable to set header with access token')

    def _process_response(self, resp):
        """ Overridden from RESTPolling - returns signals to notify """

        # By default, just return all of the signals we get, no paging
        return [Signal(d) for d in self._get_dicts_from_response(resp)], False

    def _get_dicts_from_response(self, resp):
        resp_data = resp.json()
        return resp_data['records']
