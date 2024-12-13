from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User as userModel
from django.contrib.auth.decorators import login_required
import os, time
import math
import json





@login_required(login_url='/login/')
def listNeuralNetwork(request):
    context = {}
    return render(request, 'ENNApp/listNeuralNetworks.html', context)

@login_required(login_url='/login/')
def deleteNeuralNetwork(request, userName, fileName):
    return redirect('listNeuralNetwork')

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def loadContextMessages(request,context):
    if 'messageErr' in request.session:
        context.update({"messageErr": request.session['messageErr']})
        del request.session['messageErr']
    if 'messageOk' in request.session:
        context.update({"messageOk": request.session['messageOk']})
        del request.session['messageOk']


@login_required(login_url='/login/')
def createModel(request, fileName, oldContext={}):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets", fileName)

    context = {}
    context.update(oldContext)

    if not os.path.exists(dataSetsPath):
        context.update({'secondaryMessageErr': "this file does not exist"})

    loadContextMessages(request,context)
    context.update({"datasetName": fileName})
    return render(request, 'ENNApp/createModel.html', context)



@login_required(login_url='/login/')
def executeModel(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets", request.POST["datasetName"])
    userFolderPath = os.path.join(BASE_DIR, "userFiles", request.user.username)
    context = {}

    if not os.path.exists(dataSetsPath):
        context.update({'messageErr': "this dataset does not exist"})
    else:
        try:       
            models = json.loads(request.POST["data"])
            rowData = json.loads(request.POST["rowData"])

            


        except BaseException as e:
            context.update({"messageErr": "An error occurred (" + str(e) +")"})

    if 'messageErr' not in context:
        request.session['messageOk'] = "All models have been executed successfully"
    else:
        request.session['messageErr'] = context["messageErr"]

    return HttpResponse("Ok")


@login_required(login_url='/login/')
def detailNeuralNetwork(request, fileName):
    fileBaseName = str(fileName).rstrip('.HDF5')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    infoPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "model", "info", (fileBaseName + ".info"))
                
    context = {}

    loadContextMessages(request,context)
    context.update({"datasetName": fileName})
    return render(request, 'ENNApp/neuralNetworkDetail.html', context)