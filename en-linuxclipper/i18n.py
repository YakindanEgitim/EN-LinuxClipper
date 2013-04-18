_ = None
try:
    import gettext
    gettext.textdomain('en-linuxclipper')
    _ = gettext.gettext
except:
    def dummytrans (text):
        return(text)

    _ = dummytrans