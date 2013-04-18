import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

class ENAPI:
    auth_token = "S=s1:U=65f0d:E=1457156ba3d:C=13e19a58e41:P=1cd:A=en-devtoken:V=2:H=9fb797af6aa22988ce4c3bf385bd2baf"

    client = EvernoteClient(token=auth_token, sandbox=True)

    user_store = client.get_user_store()

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
    def upload_image(image_src):
        note = Types.Note()
        note.title = "test screenshot"
        image = open(image_src, 'rb').read()
        md5 = hashlib.md5()
        md5.update(image)
        hash = md5.digest()

        data = Types.Data()
        data.size = len(image)
        data.bodyHash = hash
        data.body = image

        resource = Types.Resource()
        resource.mime = 'image/png'
        resource.data = data

        # Now, add the new Resource to the note's list of resources
        note.resources = [resource]

        # To display the Resource as part of the note's content, include an <en-media>
        # tag in the note's ENML content. The en-media tag identifies the corresponding
        # Resource using the MD5 hash.
        hash_hex = binascii.hexlify(hash)

        # The content of an Evernote note is represented using Evernote Markup Language
        # (ENML). The full ENML specification can be found in the Evernote API Overview
        # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM ' \
            '"http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>test screenshot<br/>'
        note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
        note.content += '</en-note>'

        # Finally, send the new note to Evernote using the createNote method
        # The new Note object that is returned will contain server-generated
        # attributes such as the new note's unique GUID.
        created_note = ENAPI.note_store.createNote(note)

        print "Successfully created a new note with GUID: ", created_note.guid