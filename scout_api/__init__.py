import version
import requests
import logging
import json
import sys
import yaml

__version__ = version.__version__

SCOUT_API_BASE = 'https://scoutapp.com/api/v2'


class ScoutAPI(object):
    """Create object to interact with the Scout REST API

    Args:
        api_key (str): API key generated by Scout to access the API

    Attributes:
        api_key (str): API key generated by Scout to access the API
        log (logging): logger used by the class

    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.log = logging.getLogger(__name__)

    def get_metrics(self, **kwargs):
        """
        Get the metric data based on the given filters.
        More info about the metrics API endpoint can be found here:
        http://help.scoutapp.com/v1.2/docs/api#fetching-metrics

        Args:
            metric_name (str): the non-humanized metric name
            metric_type (str): disk|memory|network|process|plugin
            metric_source_name (str): if plugin, the plugin name. If process, the process name. if disk|network, the volume/interface name
            environment (str, optional): environment name (exact match required). DEFAULT: no filtering by environment
            role (str, optional): role name (exact match required.) DEFAULT: no filtering by role
            server (str, optional): server hostname (exact match, wildcard, or regex ok)
            duration (str, optional): one of: "30 minutes", "5 hours", "12 hours", "1 day", "1 week", "2 weeks", "1 month", "3 months", "6 months", "1 year". DEFAULT: 5 hours
            display (str, optional): range|breakout. DEFAULT: range

        Returns:
            dict: result from the api call in the below format

            {u'metrics': [{u'label': u'hostname1',
                           u'points': [[0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0]],
                           u'precision': 2,
                           u'units': u''},
                          {u'label': u'hostname2',
                           u'points': [[1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0],
                                       [1.0, 1.0, 1.0]],
                           u'precision': 2,
                           u'units': u''}],
             u'num_servers': 2,
             u'step': 60,
             u'timestamps': [1433266800000,
                             1433266860000,
                             1433266920000,
                             1433266980000,
                             1433267040000,
                             1433267100000,
                             1433267160000,
                             1433267220000,
                             1433267280000,
                             1433267340000,
                             1433267400000,
                             1433267460000,
                             1433267520000,
                             1433267580000,
                             1433267640000,
                             1433267700000,
                             1433267760000,
                             1433267820000,
                             1433267880000,
                             1433267940000,
                             1433268000000,
                             1433268060000,
                             1433268120000,
                             1433268180000,
                             1433268240000,
                             1433268300000,
                             1433268360000,
                             1433268420000,
                             1433268480000,
                             1433268540000]}

        Raises:
            None
        """
        self.log.info('Getting metrics data based on the filter: {0}'.format(kwargs))
        self.log.debug(kwargs)
        data = self.__query_api('metrics.json', None, kwargs)
        return data.json()['result']

    def get_role(self):
        """
        Get the list of roles with their included servers

        Returns:
            dict: list of roles

        """
        self.log.info('Getting role data')
        data = self.__query_api('roles.json')
        return data.json()['result']

    def get_role_list(self):
        """
        Get the list of roles

        Returns:
            array: list of roles

        """
        self.log.info('Getting list of roles')
        return self.get_role()['result'].keys()

    def get_role_server_list(self, role):
        """
        Get the list of servers in a given role

        Args:
            role (str): role to lookup server list of

        Returns:
            array: server hostname list

        Raises:
            ValueError: role does not exist

        """
        self.log.info('Getting server list for the {0} role'.format(role))
        data = self.get_role()['result']
        if role in data:
            self.log.debug('Found server list for the {0} role'.format(role))
            return data[role]
        else:
            self.log.debug('Could not find server list for the {0} role'.format(role))
            raise ValueError('{0} is not a valid role'.format(role))

    def set_server_notifications(self, hostname, enabled):
        """
        Enable or disable notifications based on server hostname

        Args:
            hostname (str): server to change notifcations of
            enabled (bool): notifications enabled if true, disabled if false

        Returns:
            dict: repsonse data from ScoutApp REST API

        Raises:
            TypeError: hostname must is a str
            TypeError: enabled must is a bool

        """
        # Verify input types
        if not isinstance(hostname, str):
            raise TypeError('hostname parameter must be of type str')
        if not isinstance(enabled, bool):
            raise TypeError('enabled parameter must be of type bool')

        self.log.info('Setting notifications enabled for {0} to {1}'.format(hostname, enabled))
        post_data = 'notifications={0}'.format(str(enabled).lower())
        data = self.__query_api('servers/{0}'.format(hostname), post_data, None)
        return data.json()

    def __query_api(self, end_point, post_data=None, query_params=None):
        """
        Query the ScoutApp REST API with the given data

        Args:
            end_point (str): api endpoint to query
            post_data (str, optional): post request with given data if present, get request if absent
            query_params (dict, optional): url parameters for get requests

        Returns:
            requests.models.Response: request response object

        Raises:
            RuntimeError: API endpoint must not return a 404
            ValueError: API key must be valid
            ValueError: query_params must be valid options

        """
        # Build the full query URL and call the Scout REST API
        full_url = '{0}/{1}/{2}'.format(SCOUT_API_BASE, self.api_key, end_point)
        if post_data:
            r = requests.post(full_url, data=post_data)
            self.log.debug('__query_api payload: {0}'.format(post_data))
        else:
            r = requests.get(full_url, params=query_params)

        # Log response info for debugging purposes
        self.log.debug('__query_api url: {0}'.format(r.url.replace(self.api_key, 'XXXXX')))
        self.log.debug('__query_api status code: {0}'.format(r.status_code))
        self.log.debug('__query_api x-request-id: {0}'.format(r.headers['x-request-id']))
        self.log.debug('__query_api headers: {0}'.format(r.headers))

        # TODO: remove after done with all api endpoints
        # self.log.debug('__query_api url: {0}'.format(r.url))

        # Handle bad status codes
        if r.status_code == 401:
            raise ValueError('Invalid API key')
        elif r.status_code == 404:
            raise RuntimeError('Endpoint not found')
        elif r.status_code == 422:
            raise ValueError('Scout was unable to process the request due to an issue with the given query parameters')
        return r
