#from django.db import models
from mongoengine import *

# Create your models here.
class Book(Document):
    url = StringField(required=True)
    title = StringField(required=True)
    authors = ListField(StringField())
    issuer = StringField()
