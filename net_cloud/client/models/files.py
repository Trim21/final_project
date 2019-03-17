import peewee as pw

from ._base import BaseModel


class Files(BaseModel):
    path = pw.TextField()
    checksum = pw.TextField()
    last_modified = pw.DateTimeField()
    status = pw.IntegerField()
    progress = pw.IntegerField()
    parent = pw.IntegerField()
    size = pw.IntegerField()
