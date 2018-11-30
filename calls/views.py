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

from .serializers import CallsSerializer
from .models import Calls
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

parser_classes = (FileUploadParser, MultiPartParser, JSONParser,)
import json

# Create your views here.


##el siguiente metodo retornara toda la data de experiencias y calls en formato json
@api_view(['GET'])
def getCalls(request):

    calls=''
    try:
        calls = Calls.objects.all().values()  # or simply .values() to get all fields
        calls = list(calls)  # important: convert the QuerySet to a list object

    except calls.DoesNotExist:
        calls = None

    content = {'calls':calls,  'success': 1}
    return Response(content)



@api_view(["POST"])
def registerCall(request):
    try:
        user = request.data.get('user')
        addressee = request.data.get('addressee')
        location = request.data.get('location')
        duration_call= request.data.get('duration_call')
        origin_number = request.data.get('origin_number')

        audio1 = request.data.get('audio1')
        uploaded_file = request.FILES.get('uploaded_file', '')

        text1 = ""
        if uploaded_file:
            handle_uploaded_file(uploaded_file)
            text1 = convert_voice_to_text(uploaded_file)

        call = Calls(user=user, addressee=addressee, location=location, duration_call=duration_call, origin_number=origin_number,
                     audio=audio1,convert_to_text=text1)
        call.save()

        serializer = CallsSerializer(call)
        content = {'call': serializer.data, 'success': 1}
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




