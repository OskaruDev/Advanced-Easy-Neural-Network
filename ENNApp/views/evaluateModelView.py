from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User as userModel
from django.contrib.auth.decorators import login_required
from .neuralNetworkView import convert_size, loadContextMessages
from .datasetView import listDataset
import os, time
from ..common import neural
from ..common import preprocessing
from ..common.untils import readFile
import json



@login_required(login_url='/login/')
def listEvaluationView(request):
    downloadNeuralNetworkUrl = "/files/" + request.user.username + "/neuralNetwork/"

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    neuralNetworkPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "neuralNetwork")

    context = {}

    if not os.path.exists(neuralNetworkPath):
        context.update({'secondaryMessageErr': "You haven't any Neural Network yet"})
    else:
        neuralNetworks = []
        for file in os.listdir(neuralNetworkPath):
            filepath = os.path.join(neuralNetworkPath, file)
            if os.path.isfile(filepath):
                #Get Code and Model
                codeUrl = ""
                infoUrl = ""
                fileBaseName = str(file).removesuffix('.keras')
                modelPath = os.path.join(BASE_DIR, "userFiles", request.user.username, "model", "code", (fileBaseName + ".py"))
                infoPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "model", "info", (fileBaseName + ".info"))
                
                if(os.path.exists(modelPath)):
                    codeUrl = "/files/" + request.user.username + "/model/code/" + (fileBaseName + ".py")
                if(os.path.exists(infoPath)):
                    infoUrl = "/files/" + request.user.username + "/model/info/" + (fileBaseName + ".info")

                #Append Data
                neuralNetworks.append({
                    "name": file, 
                    "userOwner": request.user.username , 
                    "creationDate": time.ctime(os.path.getctime(filepath)), 
                    "size": convert_size(os.path.getsize(filepath)), 
                    "url": ( downloadNeuralNetworkUrl + file), 
                    "infoUrl": infoUrl,
                    "codeUrl": codeUrl
                    })
                
        context.update({'neuralNetworks': neuralNetworks})
    
    loadContextMessages(request,context)

    return render(request, 'ENNApp/evaluateSelection.html', context)





@login_required(login_url='/login/')
def evaluateDetailNeuralNetwork(request, fileName):
    fileBaseName = str(fileName).removesuffix('.keras')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    infoPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "model", "info", (fileBaseName + ".info"))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets")

    context = {}

    if not os.path.exists(infoPath):
        context.update({'secondaryMessageErr': "this file does not exist"})
    else:
       
        try:
            toRet = neural.readInfoFile(infoPath)
            print(str(toRet))
            data = json.loads(toRet)
            print(type(data))
            context.update(data)

        except BaseException as e:
            context.update({"messageErr": "An error occurred reading the file (" + str(e) +")"})
        

        #List Dataset
        if not os.path.exists(dataSetsPath):
            context.update({'secondaryMessageWarning': "You haven't any dataset yet"})
        else:              
            context.update({'datasets': listDataset(dataSetsPath)})
    
    loadContextMessages(request,context)
    context.update({"neuralNetworkName": fileName})
    context.update({"evaluateView": True})
    return render(request, 'ENNApp/neuralNetworkDetail.html', context)


@login_required(login_url='/login/')
def evaluateModel(request):
    dataset = request.POST.get("dataset")
    metric = request.POST.get("metric")
    fileName = request.POST.get("neuralNetworkName")
    rowData = json.loads(request.POST["rowData"])


    fileBaseName = str(fileName).removesuffix('.keras')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    infoFolderPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "model", "info")
    infoPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "model", "info", (fileBaseName + ".info"))
    neuralNetworkPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "neuralNetwork", (fileBaseName + ".keras"))
    datasetPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets", dataset)

    context = {}

    
    

    if not os.path.exists(infoPath):
        context.update({'secondaryMessageErr': "this file does not exist"})
    else:
       
        try:
            toRet = neural.readInfoFile(infoPath)
            print(str(toRet))
            data = json.loads(toRet)
            print(type(data))
            data = neural.evaluate(data, neuralNetworkPath, datasetPath, metric, rowData)
            context.update(data)
            neural.writeFileWithJson(data, infoFolderPath, fileBaseName + ".info")

        except BaseException as e:
            context.update({"messageErr": "An error occurred reading the file (" + str(e) +")"})
            print("ERROR: " + str(e))
    
    
    
    loadContextMessages(request,context)
    context.update({"datasetName": fileName})
    context.update({"evaluateView": True})
    return render(request, 'ENNApp/neuralNetworkDetail.html', context)





@login_required(login_url='/login/')
def selectTargetModal(request):
    fileName = request.GET["dataset"]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets", fileName)

    context = {}

    if not os.path.exists(dataSetsPath):
        context.update({'secondaryMessageErr': "this file does not exist"})
    else:
       
        try:
            toRet = preprocessing.getColsNames(dataSetsPath)
            context.update(toRet)

        except BaseException as e:
            context.update({"messageErr": "An error occurred reading the file (" + str(e) +")"})
    
    loadContextMessages(request,context)
    context.update({"datasetName": fileName})
    return render(request, 'ENNApp/selectTargetModal.html', context)

