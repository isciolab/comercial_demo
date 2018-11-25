from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Experience(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    lugar = models.CharField(max_length=255)
    pediste_info = models.BooleanField()
    audio1 = models.CharField(max_length=255)
    conversion_audio1 = models.TextField()
    audio2 = models.CharField(max_length=255)
    conversion_audio2 = models.TextField()
    flag_converted = models.BooleanField()

    @classmethod
    def create(cls, user_id, cliente, lugar, pediste_info, audio1, audio2, conversion_audio1, conversion_audio2):
        experience = cls(user_id=user_id, cliente=cliente, lugar=lugar, pediste_info=pediste_info, audio1=audio1, audio2=audio2,
                         conversion_audio1=conversion_audio1, conversion_audio2=conversion_audio2)
        # do something with the book
        return experience

    class Meta:
        db_table = "experience"


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pbx_user = models.CharField(max_length=100)
    pbx_password = models.CharField(max_length=100)

    class Meta:
        db_table = "userdetail"
