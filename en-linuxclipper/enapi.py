from gi.repository import Notify, Gtk, Gdk

import hashlib
import binascii
import subprocess

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
 
from evernote.api.client import EvernoteClient

from i18n import _
from common import HOST
from config import ConfigManager


class ENAPI:
    """
    ENAPI class doing all API communucation with Evernote.
    ENAPI is a static class, you can use it without instances with ENAPI
    namespace at anywhere of application.
    """

    access_token = ConfigManager.get_conf('access_token')
    logged = False

    # connect and disconnect functions will use this callback
    # for updating popup menu defined in Indicator class
    update_popup_menu_callback = None

    @staticmethod
    def get_username():
        """ Returns user's account name on Evernote """

        if not ENAPI.is_logged():
            return False

        return ENAPI.user.username

    @staticmethod
    def is_logged():
        """ Returns connection status of ENAPI class. """

        return ENAPI.logged

    @staticmethod
    def connect():
        """
        Connect Evernote with ENAPI.access_token and define common api
        objects, change connection status to True. This function returns False
        if given access_token expired/revoked or API version rejected by
        Evernote server.

        Returns nothing if connection were successfull.
        Both connect/disconnect functions updating Indicator's popup menu.
        """

        try:
            ENAPI.client = EvernoteClient(token=ENAPI.access_token, 
                                            sandbox=True)

            ENAPI.user_store = ENAPI.client.get_user_store()
            ENAPI.user = ENAPI.user_store.getUser(ENAPI.access_token)

            ENAPI.note_store = ENAPI.client.get_note_store()

        except Errors.EDAMUserException:
            # authentication failed
            return False

        version_ok = ENAPI.user_store.checkVersion(
            "Evernote EDAMTest (Python)",
            UserStoreConstants.EDAM_VERSION_MAJOR,
            UserStoreConstants.EDAM_VERSION_MINOR
        )
        if not version_ok:
            exit(1)

        ENAPI.logged = True

        # update popup menu
        ENAPI.update_popup_menu_callback()

    @staticmethod
    def disconnect():
        """
        Destroy all common API objects and change connection status to False
        Both connect/disconnect functions updating Indicator's popup menu.
        """

        ENAPI.client = None
        ENAPI.user_store = None
        ENAPI.user = None
        ENAPI.note_store = None

        ENAPI.logged = False

        # update popup menu
        ENAPI.update_popup_menu_callback()

    @staticmethod
    def create_note(title=None, attachment_data=None, attachment_mime=None):
        """
        Create new note with given arguments. ENAPI class must be logged to
        work.

        Keyword Arguments:
        title --- Title of new note (String)
        attachment_data --- raw binary data of attachment. (File-like object)
        attachment_mime: mime type of data, example: 'image/png' (String)

        Returns nothing.
        == TO DO: Add some error handling blocks ==
        """

        if not ENAPI.is_logged():
            return False

        note = Types.Note()
        note.title = title

        # generate hash of attachment
        md5 = hashlib.md5()
        md5.update(attachment_data)
        hash = md5.digest()

        # create data object from attachment
        data = Types.Data()
        data.size = len(attachment_data)
        data.bodyHash = hash
        data.body = attachment_data

        # add data object to note's resources
        resource = Types.Resource()
        resource.mime = attachment_mime
        resource.data = data
        note.resources = [resource]
        hash_hex = binascii.hexlify(hash)

        # generate note context
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM '
        note.content += '"http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>'
        note.content += '<en-media type="' + resource.mime
        note.content += '" hash="' + hash_hex + '"/>'
        note.content += '</en-note>'

        # create note
        created_note = ENAPI.note_store.createNote(note)

        # share note and copy link to clipboard

        message = note.title

        if ConfigManager.get_conf('copy-to-clipboard'):
            ENAPI.copy_link_to_clipboard(created_note.guid)
            message += _(' was saved, and public link copied to clipboard.')
        else:
            message += _(' was saved')

        # show notification
        Notify.init('En-LinuxClipper')
        notification = Notify.Notification.new(
            _('Upload Finished'),
            message,
            _('dialog-information')
        )
        notification.show()

        # play finish sound
        if ConfigManager.get_conf('play-sound'):
            subprocess.call(['/usr/bin/canberra-gtk-play',
                            '--id', 'dialog-information'])

    @staticmethod
    def set_access_token(access_token):
        """
        This function updates access_token of ENAPI class when user logged to
        Evernote. Also saves it with ConfigManager.

        Keyword Arguments:
        access_token --- New access token (String)
        """

        ENAPI.access_token = access_token
        ENAPI.connect()

        ConfigManager.set_conf('access_token', access_token)
        ConfigManager.save_config()

    @staticmethod
    def copy_link_to_clipboard(guid):
        """
        Generate sharing url of note and copy it to X Clipboard.
        Attention: Shared notes will be public.

        Keyword Arguments:
        guid --- Note identifier (String)

        == TO DO: Add some error handling blocks ==
        """
        
        shareKey = ENAPI.note_store.shareNote(ENAPI.access_token, guid)
        url = "https://%s/shard/%s/sh/%s/%s" % (HOST, ENAPI.user.shardId,
                                                 guid, shareKey)

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(url, len(url))
