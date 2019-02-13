import platform
import sys
import urllib
import urllib2
from urllib2 import HTTPError
import json
from .models.postmark_exception import PostmarkException


class PostmarkClientBase:

    base_url = 'https://api.postmarkapp.com'
    # base_url = 'http://postb.in/Zfx8Vo1N'
    authorization_token = None
    authorization_header = None
    version = None
    os = None
    timeout = 30

    def __init__(self):
        pass

    def _setup(self, token, header, timeout=30):
        self.authorization_token = token
        self.authorization_header = header
        version = sys.version_info
        self.version = "{}.{}.{}".format(version[0], version[1], version[2])
        self.os = platform.system()
        self.timeout = timeout

    def _process_rest_request(self, method=None, path=None, body={}):
        options = {
            'headers': {
                'User-Agent': 'PyPostmark (Python Version:{}, OS:{}'.format(self.version, self.os),
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                self.authorization_header: self.authorization_token
            },
            'query': {},
            'json': {}
        }

        query_methods = ['GET', 'HEAD', 'DELETE', 'OPTIONS']
        body_methods = ['PUT', 'POST', 'PATCH']

        if method not in query_methods and method not in body_methods:
            raise Exception("Method {}".format(method) + " is not supported.")

        if len(body) > 0:
            clean_params = {}
            for bk, bv in body.iteritems():
                if bv is not None:
                    clean_params[bk] = bv

            if method in query_methods:
                options['query'] = clean_params
            else:
                options['json'] = clean_params

        url = self.base_url + path
        if method in query_methods:
            url += '?' + urllib.urlencode(options['query'])
            request = urllib2.Request(
                url=url,
                headers=options['headers']
            )
        else:
            request = urllib2.Request(
                url=url,
                data=json.dumps(options['json']),
                headers=options['headers']
            )
        try:
            response_data = urllib2.urlopen(request, timeout=self.timeout).read()
            return json.loads(response_data)
        except HTTPError, e:
            if e.code == 401:
                raise PostmarkException(
                    message='Unauthorized: Missing or incorrect API token in header. Please verify that you used the '
                            'correct token when you constructed your client.',
                    http_status_code=401
                )
            elif e.code == 500:
                raise PostmarkException(
                    message='Internal Server Error: This is an issue with Postmark\'s servers processing your request. '
                            'In most cases the message is lost during the process, and Postmark is notified so that '
                            'we can investigate the issue.',
                    http_status_code=500
                )
            elif e.code == 503:
                raise PostmarkException(
                    message='The Postmark API is currently unavailable, please try your request later.',
                    http_status_code=503
                )
            else:
                decoded = json.loads(e.read())
                raise PostmarkException(
                    message=decoded['Message'],
                    http_status_code=e.code,
                    postmark_api_error_code=decoded['ErrorCode']
                )
