from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from time import gmtime, strftime
# Create your models here.

class Calls(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=255)
    addressee= models.CharField(max_length=255)
    calldate = models.DateTimeField(default=datetime.now(),blank=True)
    location = models.CharField(max_length=255)
    duration_call = models.CharField(max_length=255)
    origin_number = models.CharField(max_length=255)
    audio = models.CharField(max_length=255,null=True)
    convert_to_text = models.TextField(null=True)
    prediction = models.TextField(null=True)

    @classmethod
    def create(cls, user, addressee, location, duration_call, origin_number, audio, convert_to_text):
        calls = cls(user=user, addressee=addressee, location=location, duration_call=duration_call, origin_number=origin_number,
                   audio=audio,convert_to_text=convert_to_text,prediction=prediction,calldate=calldate)
        # do something with the book
        return calls

    class Meta:
        db_table = "calls"


