import sys
from subprocess import call

from django.core.files.storage import default_storage
from django.shortcuts import render

from django.http import Http404, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
import base64
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
##from rest_framework import serializers
from django.conf import settings
from django.db.models import Count, Avg, Sum  ##para poder hacer el group by

from .serializers import CallsSerializer
from .models import Calls
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

parser_classes = (FileUploadParser, MultiPartParser, JSONParser,)
import json
import os.path  ##libreria que verifica si los archivos existen
from pysftp import Connection, CnOpts

rutainputdropbox = "/home/jsonfiles/uploads/input"
rutaouputdropbox = "/home/jsonfiles/uploads/ouput"


# Create your views here.

##el siguiente metodo retornara toda la data de experiencias y calls en formato json
@api_view(['GET'])
def getCalls(request):
    calls = ''
    try:

        cnopts = CnOpts()
        cnopts.hostkeys = None
        with Connection('88.208.3.175'
                , username='jsonfiles'
                , password='5DyfKTFFc3dbksv'
                , port=222
                , cnopts=cnopts
                        ) as sftp:
            filelist = sftp.listdir('/input')
            print(filelist)
            # dirlist = sftp.listdir(remotepath=full_path)



    except ObjectDoesNotExist:
        calls = None

    content = {'calls': calls, 'success': 1}
    return Response(content)


@api_view(['GET'])
def urlcron(request):
    content = {'success': 1}
    return Response(content)


@api_view(["POST"])
def registerCall(request):
    try:
        user = request.data.get('user')
        addressee = request.data.get('addressee')
        location = request.data.get('location')
        duration_call = request.data.get('duration_call')
        origin_number = request.data.get('origin_number')

        audio1 = request.data.get('audio1')
        uploaded_file = request.FILES.get('uploaded_file', '')

        text1 = ""
        if uploaded_file:
            handle_uploaded_file(uploaded_file)
            text1 = convert_voice_to_text(uploaded_file)
            audio1 = audio1[:-4] + ".flac"

        call = Calls(user=user, addressee=addressee, location=location, duration_call=duration_call,
                     origin_number=origin_number,
                     audio=audio1, convert_to_text=text1)
        call.save()

        serializer = CallsSerializer(call)
        content = {'call': serializer.data, 'success': 1}

        ##escribo el archivo en la ruta de dropbox
        try:
            print('voy a escribir el archivo calls' + str(serializer.data['id']))
            if text1 != "":
                with open(rutainputdropbox + '/calls' + str(serializer.data['id']) + '.json', 'w') as outfile:
                    json.dump(serializer.data, outfile)

        except Exception:
            print ("No se subio el archivo")
        return Response(content)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


##este metodo lee el archivo json de la carpeta ouput
@api_view(['GET'])
def readfileouput(request):
    data = ""
    content = {'success': 1}
    ##busco los archivos den la ruta del dropbox
    files = os.listdir(rutaouputdropbox)
    print(files)
    if len(files) > 0:
        for file in files:
            ##si empiezan con "c" es que son los calls
            if file[:1] == "c":
                with open(rutaouputdropbox + '/' + file) as f:
                    ##aqui obtengo el archivo
                    data = json.load(f)
                    call = ''
                    try:
                        ##busco el registro de la llamada
                        call = Calls.objects.get(id=data[0]['id'])
                    except Calls.DoesNotExist:
                        call = ""

                    # le actualizo la prediccion
                    if call != "":
                        call.prediction = str(data[0]['pred'])
                        call.save()

                    # elimino el archivo
                    os.remove(rutaouputdropbox + '/' + file)



    else:
        content['success'] = 0
    return Response(content)


# retorna el promedio de las llamadas por comercial
@api_view(['GET'])
def promediocall(request):
    try:

        query = Calls.objects.all().values()
        query = query.values('user').annotate(Avg("duration_call")).order_by('user')
        pickup_records = []

        for row in query:
            record = [row['user'], row['duration_call__avg']]
            pickup_records.append(record)

        content = {'calls': pickup_records, 'success': 1}

        return Response(content)
    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


##este metodo retorna los datos de la llamada por un rango de fecha y por comercial
@api_view(['POST'])
def getAllSentim(request):
    try:
        comercial = request.data.get('comercial', '')
        desde = request.data.get('desde', '')
        hasta = request.data.get('hasta', '')

        query = Calls.objects.all().values()
        if desde != "":
            ##query= Calls.objects.annotate(calldate__gte=desde)
            query = query.filter(calldate__gte=desde)

        if hasta != "":
            query = query.filter(calldate__lt=hasta)

        if comercial != "":
            query = query.filter(user=comercial)

        if query != "":
            # query = list(query)
            ###query = serializers.serialize('json', query)
            queryfechas = query.extra(select={'date': "DATE(calldate)"}). \
                values('date'). \
                annotate(count_items=Count('calldate')) \
                .order_by('date')

            query = query.extra(select={'date': "DATE(calldate)"}). \
                values('date', 'prediction'). \
                annotate(count_items=Count('calldate')) \
                .order_by('date')

            pickup_dict = []
            record = {"name": "NEUTRO", "data": []}
            pickup_dict.append(record)

            record = {"name": "POSITIVO", "data": []}
            pickup_dict.append(record)

            record = {"name": "negativo", "data": []}
            pickup_dict.append(record)

            fechas = []  ##arreglo para almacenar la fecha

            contneutro = 0
            contposit = 0
            contnegat = 0
            cont = 0
            ##recorro todas las fechas que tienen resultado
            if len(queryfechas) > 0:
                for resultfechas in queryfechas:

                    ##recorro los resultados agrupados por fecha y por Predicciones
                    if len(query) > 0:
                        for result in query:

                            if resultfechas['date'] == result['date']:

                                if result['prediction'] == "NEUTRO":
                                    ##pickup_dict[0]['data'][contneutro] = result['count_items']
                                    pickup_dict[0]['data'].append(result['count_items'])
                                    contneutro = contneutro + 1
                                if result['prediction'] == "POSITIVO":
                                    ##pickup_dict[1]['data'][contposit]=result['count_items']
                                    pickup_dict[1]['data'].append(result['count_items'])
                                    contposit = contposit + 1
                                if result['prediction'] == "NEGATIVO":
                                    ##pickup_dict[2]['data'][contnegat]=result['count_items']
                                    pickup_dict[2]['data'].append(result['count_items'])
                                    contnegat = contnegat + 1

                        if cont == contneutro:
                            pickup_dict[0]['data'].append(0)
                            contneutro = contneutro + 1
                        if cont == contposit:
                            pickup_dict[1]['data'].append(0)
                            contposit = contposit + 1
                        if cont == contnegat:
                            pickup_dict[2]['data'].append(0)
                            contnegat = contnegat + 1
                        cont = cont + 1

                        fechas.append(resultfechas['date'])

        content = {'calls': pickup_dict, 'fechas': fechas, 'success': 1}

        return Response(content)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def convert_voice_to_text(f):
    # try:
    print('convirtiendo audio')
    # Instantiates a client
    audio = f.name[:-4] + ".flac"
    file_name = "/home/ciudatos/uploads/audios/" + audio

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
        # sample_rate_hertz=8000,
        language_code='es-ES')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    print(response.results)
    text = ""

    print(response.results)
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        text = text + format(result.alternatives[0].transcript)

    print(text)
    return text


# except Exception:
#    print ("error convirtiendo")
#    return ""


def handle_uploaded_file(f):
    # file_number es el numero del audio, ejemplo, si file_number es 1 buscar en el campo audio1
    file_path = "/home/ciudatos/uploads/audios/"
    with open(file_path + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            audiofile_byte = base64.b64decode(chunk)
            destination.write(audiofile_byte)
            # mp3_list = get_mp3_list("/home/ciudatos/uploads/")
            # print(mp3_list)
            convert_mp3("/home/ciudatos/uploads/audios/" + f.name)


# convert mp3 to flac if the flac target file does not already exist
def convert_mp3(mp3):
    # for mp3 in mp3_list:
    flac = mp3[:-4] + ".flac"
    if os.path.isfile(flac):
        print('File ' + flac + ' already exists')
    else:
        # call(["ffmpeg", "-i ", mp3, "-ac 1", flac])
        call('ffmpeg -i ' + mp3 + ' -qscale 0 -ac 1 ' + str(flac), shell=True)
        # call('ffmpeg -i '+mp3+' -filter_complex channelsplit=channel_layout=stereo ' + str(flac), shell=True)
