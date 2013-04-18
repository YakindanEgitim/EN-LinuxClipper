from gi.repository import Notify
import hashlib
import binascii
import datetime
import subprocess
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

from i18n import _

class ENAPI:
    auth_token = "S=s1:U=65f0d:E=1457156ba3d:C=13e19a58e41:P=1cd:A=en-devtoken:V=2:H=9fb797af6aa22988ce4c3bf385bd2baf"

    client = EvernoteClient(token=auth_token, sandbox=True)

    user_store = client.get_user_store()

    user = user_store.getUser(auth_token)

    version_ok = user_store.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )
    if not version_ok:
        exit(1)

    note_store = client.get_note_store()

    @staticmethod
    def get_notebooks():
        return note_store.listNotebooks()

    @staticmethod
    def upload_image(image):
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

        created_note = ENAPI.note_store.createNote(note)
        print ENAPI.get_note_link(created_note.guid)
        Notify.init('En-LinuxClipper')
        notification = Notify.Notification.new(
                _('Upload Finished'),
                note.title + _(' was saved, and link copied to clipboard.'),
                _('dialog-information')
            )
        notification.show()
        subprocess.call(['/usr/bin/canberra-gtk-play','--id','dialog-information'])

    @staticmethod
    def get_note_link(guid):
        shareKey = ENAPI.note_store.shareNote(ENAPI.auth_token, guid)
        return "https://sandbox.evernote.com/shard/%s/sh/%s/%s" % (ENAPI.user.shardId, guid, shareKey)