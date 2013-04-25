from gi.repository import Gtk
from gi.repository import WebKit

import oauth2 as oauth
import urllib
import urlparse

from i18n import _
from common import CONSUMER_KEY, CONSUMER_SECRET, HOST
from enapi import ENAPI


class AuthWin(Gtk.Window):
    """ 
    This class is Window object containing web browser. 
    And will be used for authentication.
    """

    def __init__(self):

        super(AuthWin, self).__init__()

        # get_oauth_url function will update this variables after generated new
        # authentication session.
        self.oauth_token = ''
        self.oauth_secret = ''

        # add webkit object inside scrolledwindow
        self.web = WebKit.WebView()
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.add(self.web)
        self.add(self.scrolled)

        # set size and position stuff
        self.set_size_request(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title(_("Authorize"))
        self.set_skip_taskbar_hint(True)
        self.set_resizable(False)
        self.set_default_size(640, 480)

        # see details about this event in callback function.
        self.web.connect('navigation-policy-decision-requested', 
            self.webkit_navigation_callback)

        # generate authentication url and load it with webkit.
        self.web.load_uri(self.get_oauth_url())
        self.show_all()

    def webkit_navigation_callback(self, frame, request, action, *args):
        """
        This event triggered when WebKit got new url to open, we are 
        using this to check if Evernote redirected user to our callback url.
        """

        url = action.get_uri()

        # check if new url containig callback url
        if "en-linuxclipper" in url:
            self.hide()

            # parse verifier string from url
            oauth_verifier = url.split('oauth_verifier=')[-1]

            # gennerate new oauth object with verifier to get access token
            token = oauth.Token(self.oauth_token, self.oauth_secret)
            token.set_verifier(oauth_verifier)

            consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
            client = oauth.Client(consumer, token)

            # do request for access token
            resp, content = client.request('https://%s/oauth' % HOST, 'POST')
            access_token = dict(urlparse.parse_qsl(content))

            ENAPI.set_access_token(access_token['oauth_token'])

        return False

    def get_oauth_url(self):
        """ 
        Generate OAuth verification url with consumer keys defined in common.py
        Returns: OAuth Url (String)
        """

        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer)

        # set http://en-linuxclipper/ as dummy callback url
        # we will catch this url with webkit events.
        resp, content = client.request(('https://%s/oauth?oauth_callback=' % HOST) + urllib.quote('http://en-linuxclipper/'), 'GET')

        data = dict(urlparse.parse_qsl(content))

        # update common oauth variables.
        self.oauth_token = data['oauth_token']
        self.oauth_secret = data['oauth_token_secret']

        return 'http://%s/OAuth.action?oauth_token=' % HOST + urllib.quote(data['oauth_token'])
