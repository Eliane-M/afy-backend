from django.core.files.storage import Storage
from firebase_admin import storage 

class FirebaseStorage(Storage):
    def __init__(self, options=None):
        if options is None:
            options = {}
        self.bucket = storage.bucket(options.get("storageBucket"))
    

    def _open(self, name, mode="rb"):
        file_blob = self.bucket.blob(name)
        return file_blob.download_as_text()

    def _save(self, name, content):
        file_blob = self.bucket.blob(name)
        file_blob.upload_from_string(content.read())
        file_blob.make_public()
        return name

    def delete(self, name):
        file_blob = self.bucket.blob(name)
        file_blob.delete()

    def exists(self, name):
        file_blob = self.bucket.blob(name)
        return file_blob.exists()

    def url(self, name):
        file_blob = self.bucket.blob(name)
        return file_blob.public_url