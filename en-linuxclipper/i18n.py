_ = None
try:
    import gettext
    gettext.textdomain('en-linuxclipper')
    _ = gettext.gettext
except ImportError:
    def dummytrans (text):
        """ Return argument without change """
        return(text)

    _ = dummytrans