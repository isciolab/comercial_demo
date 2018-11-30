from django.core.files.storage import default_storage
from django.shortcuts import render

from django.http import Http404, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from rest_framework.decorators import api_view, authentication_classes, permission_classes
import io
import os
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from django.core import serializers
from rest_framework import serializers
from django.conf import settings

from .serializers import ExperienceSerializer, UserSerializer, UserDetailSerializer
from calls.serializers import CallsSerializer
from .models import Experience, UserDetail
from calls.models import Calls
#import numpy as np
#import matplotlib.pyplot as plt
#from wordcloud import WordCloud

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

parser_classes = (FileUploadParser, MultiPartParser, JSONParser,)
import json

# Create your views here.


##el siguiente metodo retornara toda la data de experiencias y calls en formato json
@api_view(['GET'])
def getExpAndCalls(request):
    experiences=''
    calls=''
    try:
        experiences = Experience.objects.all().values()  # or simply .values() to get all fields
        experiences = list(experiences)  # important: convert the QuerySet to a list object

        calls = Calls.objects.all().values()  # or simply .values() to get all fields
        calls = list(calls)  # important: convert the QuerySet to a list object

    except experiences.DoesNotExist:
        calls = None
        experiences = None

    content = {'experiences': experiences,'calls':calls,  'success': 1}
    return Response(content)



@api_view(["POST"])
def RegisterExperience(request):
    try:
        user = request.data.get('user')
        cliente = request.data.get('cliente')
        lugar = request.data.get('lugar')
        pediste_info = request.data.get('pediste_info')
        audio1 = request.data.get('audio1')
        audio2 = request.data.get('audio2')
        uploaded_file = request.FILES.get('uploaded_file', '')
        uploaded_file2 = request.FILES.get('uploaded_file2', '')

        text1 = ""
        text2 = ""
        if uploaded_file:
            handle_uploaded_file(uploaded_file)
            text1 = convert_voice_to_text(uploaded_file)

        if uploaded_file2:
            handle_uploaded_file(uploaded_file2)
            text2 = convert_voice_to_text(uploaded_file2)

        experience = Experience(user=user, cliente=cliente, lugar=lugar, pediste_info=pediste_info, audio1=audio1, audio2=audio2,
                                flag_converted=0, conversion_audio1=text1, conversion_audio2=text2)
        experience.save()

        serializer = ExperienceSerializer(experience)
        content = {'experience': serializer.data, 'success': 1}
        return Response(content)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def convert_voice_to_text(f):
    print('convirtiendo audio')
    # Instantiates a client
    file_name = "/home/ciudatos/pythonapp/uploads/audios/" + f.name
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = file_name

    print(file_name)
    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,

        language_code='es-ES')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    text = format(response.results[0].alternatives[0].transcript)
    print(text)

    #for result in response.results:
    #    print('Transcript: {}'.format(result.alternatives[0].transcript))
    return text


def handle_uploaded_file(f):
    #file_number es el numero del audio, ejemplo, si file_number es 1 buscar en el campo audio1
    file_path = "/home/ciudatos/pythonapp/uploads/audios/"
    with open(file_path + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



@api_view(['POST'])
def custom_login(request, format=None):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        try:
            userdetail = UserDetail.objects.get(user=user.id)
        except UserDetail.DoesNotExist:
            userdetail = None

        serializer = UserSerializer(user)
        serializerdetail = UserDetailSerializer(userdetail)
        content = {'user': serializer.data, 'userdetail':serializerdetail.data, 'success': 1}
    else:
        content = {'success': 0}

    return Response(content)






