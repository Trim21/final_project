import peewee as pw

from ._base import BaseModel


class Dirs(BaseModel):
    path = pw.TextField()
    name = pw.TextField()
    parent = pw.IntegerField()
    size = pw.IntegerField()
