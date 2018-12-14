import sys
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
from rest_framework import serializers
from django.conf import settings

from .serializers import ExperienceSerializer, UserSerializer, UserDetailSerializer
from calls.serializers import CallsSerializer
from .models import Experience, UserDetail
from calls.models import Calls
# import numpy as np
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
from subprocess import call
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pprint import PrettyPrinter

parser_classes = (FileUploadParser, MultiPartParser, JSONParser,)
import json  ##para retornar data en json
import requests
import os.path  ##libreria que verifica si los archivos existen
import datetime
from django.db.models import Count  ##para poder hacer el group by

rutainputdropbox = "C:/Users/fernando/Dropbox/demo/input"
##rutainputdropbox="/root/Dropbox/demo/input"
##rutainputdropbox="/root/Dropbox/demo/input"
rutaouputdropbox = "/root/Dropbox/demo/ouput"
##rutaouputdropbox = "C:/Users/fernando/Dropbox/demo/ouput"


##el siguiente metodo retornara toda la data de experiencias y calls en formato json
@api_view(['GET'])
def getexpandcalls(request):
    experiences = ''
    calls = ''
    try:
        experiences = Experience.objects.all().values()  # or simply .values() to get all fields
        experiences = list(experiences)  # important: convert the QuerySet to a list object

        calls = Calls.objects.all().values()  # or simply .values() to get all fields
        calls = list(calls)  # important: convert the QuerySet to a list object

        for attr in calls:

            print(attr['id'])
            with open(rutainputdropbox + '/calls' + str(attr['id']) + '.json', 'w') as outfile:
                json.dump(attr, outfile, default=cnvertirfecha)
                print("se imrpimiooooooooooooooooo")




    except experiences.DoesNotExist:
        calls = None
        experiences = None

    print(os.path.isdir(rutainputdropbox))
    content = {'experiences': experiences, 'calls': calls, 'success': 1}
    try:
        with open(rutainputdropbox + '/data.json', 'w') as outfile:
            json.dump(content, outfile, default=cnvertirfecha)

    except ValueError as e:
        print ("No se subio el archivo call.json")
        print(e.args[0])
    return Response(content)


##los dos siguientes metodos, son pruebas para convertir las fechas datetime, ya que al intentar serializarlas,
##con el json.dump, dice que no se puede serializar datetime. Cualquiera de ;as dos funcionan
def myconverter(o):
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()


def cnvertirfecha(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


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
            ##si empiezan con "e" es que son las experiencias
            if file[:1] == "e":
                with open(rutaouputdropbox + '/' + file) as f:
                    ##aqui obtengo el archivo
                    data = json.load(f)

                    ##busco el registro de la llamada, y le actualizo la prediccion
                    experiencia = Experience.objects.get(id=data[0]['id'])
                    experiencia.prediction = data[0]['pred']
                    experiencia.save()

    else:
        content['success'] = 0
    return Response(content)


##metodo que hace el print de un objeto o arreglo, en la consola
def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


@api_view(['GET'])
def getDataByCecula(request):
    cedula = 1032398833
    res = 1;
    response_data = {}
    try:
        ##/api/report_json/<id>.
        url = 'https://sosorno@isciolab.com:SCHsas2018@dash-board.tusdatos.co/api/results/'
        url = 'https://sosorno@isciolab.com:SCHsas2018@dash-board.tusdatos.co/api/results/97bb6e9e-d26b-45c4-961d-b28836167133'
        url = 'https://sosorno@isciolab.com:SCHsas2018@dash-board.tusdatos.co/api/report_json/5c0752e0c39de82fe678beb4'
        ##url ='http://127.0.0.1:8000/experience/getexpandcalls'

        response_data['cedula'] = cedula
        ## response_data['message'] = 'Datos devueltos'

        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        ##res = requests.post(url, data=json.dumps(response_data), headers=headers)
        res = requests.get(url, headers=headers)
        ##res=requests.get(url)

        print(dump(res))
        print("prueaaaaaaaaaaaaaaa")
        print(res)

    except Exception as e:
        response_data['success'] = 0
        response_data['error'] = "Ha ocurrido un error al realizar la solicitud"
        res = response_data

    return Response(res)


@api_view(["POST"])
def RegisterExperience(request):
    try:

        user = request.data.get('user', '')
        cliente = request.data.get('cliente')
        lugar = request.data.get('lugar')
        pediste_info = request.data.get('pediste_info')
        audio1 = request.data.get('audio1')
        audio2 = request.data.get('audio2')
        uploaded_file = request.FILES.get('uploaded_file', '')
        uploaded_file2 = request.FILES.get('uploaded_file2', '')
        expedate = request.data.get('fecha')

        # print(request.FILES)
        # print(uploaded_file.size)
        # print(audio1)
        text1 = ""
        text2 = ""
        if uploaded_file:
            handle_uploaded_file(uploaded_file)
            text1 = convert_voice_to_text(uploaded_file)
            audio1 = audio1[:-4] + ".flac"

        if uploaded_file2:
            handle_uploaded_file(uploaded_file2)
            text2 = convert_voice_to_text(uploaded_file2)
            audio2 = audio2[:-4] + ".flac"

        experience = Experience(user=user, cliente=cliente, lugar=lugar, pediste_info=pediste_info, audio1=audio1,
                                audio2=audio2, expedate=expedate,
                                flag_converted=0, conversion_audio1=text1, conversion_audio2=text2)
        experience.save()

        serializer = ExperienceSerializer(experience)
        content = {'experience': serializer.data, 'success': 1}

        ##escribo el archivo en la ruta de dropbox
        with open(rutainputdropbox + '/experience' + str(serializer.data['id']) + '.json', 'w') as outfile:
            json.dump(serializer.data, outfile)

        return Response(content)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def convert_voice_to_text(f):
    try:
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

        text = ""
        print(response.results)
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))
            text = text + format(result.alternatives[0].transcript)

        print(text)

        # for result in response.results:
        # print('Transcript: {}'.format(text.alternatives[0].transcript))
        return text
    except Exception:
        print ("error convirtiendo")
        return ""


def handle_uploaded_file(f):
    # audiofile_byte = base64.b64decode(f)

    print(f.name)
    # file_number es el numero del audio, ejemplo, si file_number es 1 buscar en el campo audio1
    file_path = "/home/ciudatos/uploads/audios/"
    with open(file_path + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            audiofile_byte = base64.b64decode(chunk)
            destination.write(audiofile_byte)
            # mp3_list = get_mp3_list("/home/ciudatos/uploads/")
            # print(mp3_list)
            convert_mp3("/home/ciudatos/uploads/audios/" + f.name)


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
        content = {'user': serializer.data, 'userdetail': serializerdetail.data, 'success': 1}
    else:
        content = {'success': 0}

    return Response(content)


# show variables (for troubleshooting)
def show_vars(target_dir):
    print('target_dir = ' + target_dir)
    print('target_dir (absolute) = ' + os.path.abspath(target_dir))


# get full list of mp3 files from your target directory
def get_mp3_list(target_dir):
    mp3_list = []
    for root, dirs, files in os.walk(target_dir):
        print(root)
        print(dirs)
        for dir in dirs:
            path = root + dir
            print(path)
            for file in os.listdir(path):
                if file.endswith(".3gp"):
                    return_data = path + "/" + file
                    print(return_data)
                    mp3_list.append(return_data)
    return mp3_list


# convert mp3 to flac if the flac target file does not already exist
def convert_mp3(mp3):
    # for mp3 in mp3_list:
    flac = mp3[:-4] + ".flac"
    if os.path.isfile(flac):
        print('File ' + flac + ' already exists')
    else:
        # call(["ffmpeg", "-i", mp3, flac])
        call('ffmpeg -i ' + mp3 + ' -ac 1 ' + str(flac), shell=True)




##este metodo retorna los datos de la llamada por un rango de fecha y por comercial
@api_view(['POST'])
def getAllSentim(request):
    try:
        comercial = request.data.get('comercial', '')
        desde = request.data.get('desde', '')
        hasta = request.data.get('hasta', '')

        query = Experience.objects.all().values()
        if desde != "":
            ##query= Calls.objects.annotate(calldate__gte=desde)
            query = query.filter(expedate__gte=desde)

        if hasta != "":
            query = query.filter(expedate__lt=hasta)

        if comercial != "":
            query = query.filter(user=comercial)

        if query != "":
            # query = list(query)
            ###query = serializers.serialize('json', query)
            queryfechas = query.extra(select={'date': "DATE(expedate)"}). \
                values('date'). \
                annotate(count_items=Count('expedate')) \
                .order_by('date')

            query = query.extra(select={'date': "DATE(expedate)"}). \
                values('date', 'prediction'). \
                annotate(count_items=Count('expedate')) \
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

        content = {'experiences': pickup_dict, 'fechas': fechas, 'success': 1}

        return Response(content)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
