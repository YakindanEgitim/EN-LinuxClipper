from gi.repository import Gtk
from gi.repository import WebKit

from i18n import _

class AuthWin(Gtk.Window):
    def __init__(self):
        super(AuthWin, self).__init__()

        self.web = WebKit.WebView()
        self.add(self.web)

        self.set_size_request(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title(_("Login to Evernote"))
        self.set_skip_taskbar_hint(True)
        self.set_resizable(False)
        self.set_default_size(640, 480)
        self.web.load_uri("https://sandbox.evernote.com")
        self.show_all()