from gi.repository import Gtk
from gi.repository import WebKit

import oauth2 as oauth
import urllib
import urlparse

from i18n import _
from common import CONSUMER_KEY, CONSUMER_SECRET, HOST
from enapi import ENAPI

class AuthWin(Gtk.Window):
    def __init__(self):
        super(AuthWin, self).__init__()

        self.oauth_token = ''
        self.oauth_secret = ''

        self.web = WebKit.WebView()
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.add(self.web)
        self.add(self.scrolled)

        self.set_size_request(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title(_("Authorize"))
        self.set_skip_taskbar_hint(True)
        self.set_resizable(False)
        self.set_default_size(640, 480)
        self.web.connect('navigation-policy-decision-requested', self.webkit_navigation_callback)        
        self.web.load_uri(self.get_oauth_url())
        self.show_all()

    def webkit_navigation_callback(self, frame, request, action, *args):
        url = action.get_uri()
        if "en-linuxclipper" in url:
            self.hide()

            oauth_verifier = url.split('oauth_verifier=')[-1]

            token = oauth.Token(self.oauth_token, self.oauth_secret)
            token.set_verifier(oauth_verifier)

            consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
            client = oauth.Client(consumer, token)

            resp, content = client.request('https://%s/oauth' % HOST, 'POST')
            access_token = dict(urlparse.parse_qsl(content))
            
            ENAPI.set_access_token(access_token['oauth_token'])

        return False

    def get_oauth_url(self):
        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer)

        # set http://en-linuxclipper/ as dummy callback url
        # we will catch this url with webkit events.
        resp, content = client.request('https://%s/oauth?oauth_callback=' % HOST + urllib.quote('http://en-linuxclipper/'), 'GET')

        data = dict(urlparse.parse_qsl(content))
        
        self.oauth_token = data['oauth_token']
        self.oauth_secret = data['oauth_token_secret']

        return 'http://%s/OAuth.action?oauth_token=' % HOST + urllib.quote(data['oauth_token'])
        