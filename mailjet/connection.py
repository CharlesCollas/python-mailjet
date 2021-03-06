import urllib
import urllib2
import base64
import httplib
from mailjet.conf import settings

class Connection(object):
    def __init__(self, access_key=None, secret_key=None, timeout=None):
        self.access_key = access_key or settings.API_KEY
        self.secret_key = secret_key or settings.SECRET_KEY
        self.timeout = timeout or settings.TIMEOUT
        self.opener = None

    def get_opener(self, url):
        if not self.opener:
            # Add the authentication data to a password manager
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(
                'Mailjet API',
                settings.URL,
                self.access_key,
                self.secret_key,
            )
            password_mgr.add_password(
                'Provide an apiKey and secretKey',
                settings.URL,
                self.access_key,
                self.secret_key,
            )
            # Create a handler for this password manager
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            # Create an opener for the handler
            self.opener = urllib2.build_opener(handler)

        return self.opener

    def open(self, method, function, options=None, postdata=None):
        url = u'%s%s%s' % (settings.URL, method, function)
        default_options = {
            'output': 'json',
        }
        if options:
            default_options.update(options)

        url += '?' + urllib.urlencode(default_options)
        if postdata:
            poststring = urllib.urlencode(postdata.items())
        else:
            poststring = None

    	request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self.access_key, self.secret_key)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        r = urllib2.urlopen(request)

        return r

    @classmethod
    def get_connection(cls, access_key, secret_key):
        return Connection(access_key, secret_key)
  
