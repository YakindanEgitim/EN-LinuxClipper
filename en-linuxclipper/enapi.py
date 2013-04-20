from gi.repository import Notify, Gtk, Gdk

import hashlib
import binascii
import datetime
import subprocess

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

from evernote.api.client import EvernoteClient

from i18n import _
from common import HOST

class ENAPI:
    access_token = ""
    logged = False

    @staticmethod
    def get_username():
        if not ENAPI.is_logged():
            return False

        return ENAPI.user.username

    @staticmethod
    def is_logged():
        return ENAPI.logged

    @staticmethod
    def connect():
        try:
            ENAPI.client = EvernoteClient(token=ENAPI.access_token, sandbox=True)
            
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

    @staticmethod
    def disconnect():
        ENAPI.client = None
        ENAPI.user_store = None
        ENAPI.user = None
        ENAPI.note_store = None

        ENAPI.logged = False

    @staticmethod
    def upload_image(image):
        if not ENAPI.is_logged():
            return False

        note = Types.Note()

        now = datetime.datetime.now()
        note.title = _("Screenshot ") + now.strftime("%Y-%m-%d %H:%M")

        # prepare raw image data for upload
        md5 = hashlib.md5()
        md5.update(image)
        hash = md5.digest()
        data = Types.Data()
        data.size = len(image)
        data.bodyHash = hash
        data.body = image

        # set mime type of image
        resource = Types.Resource()
        resource.mime = 'image/png'
        resource.data = data

        # add image data to resource list of note
        note.resources = [resource]
        hash_hex = binascii.hexlify(hash)

        # generate note context
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM '
        note.content += '"http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>'
        note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
        note.content += '</en-note>'

        # do upload
        created_note = ENAPI.note_store.createNote(note)

        # share note and copy link to clipboard
        ENAPI.copy_link_to_clipboard(created_note.guid)

        # show notification
        Notify.init('En-LinuxClipper')
        notification = Notify.Notification.new(
                _('Upload Finished'),
                note.title + _(' was saved, and link copied to clipboard.'),
                _('dialog-information')
            )
        notification.show()

        # play finish song
        subprocess.call(['/usr/bin/canberra-gtk-play','--id','dialog-information'])

    @staticmethod
    def set_access_token(access_token):
        ENAPI.access_token = access_token
        ENAPI.connect()

    @staticmethod
    def copy_link_to_clipboard(guid):
        shareKey = ENAPI.note_store.shareNote(ENAPI.access_token, guid)
        url = "https://%s/shard/%s/sh/%s/%s" % (HOST, ENAPI.user.shardId, guid, shareKey)

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(url, len(url))