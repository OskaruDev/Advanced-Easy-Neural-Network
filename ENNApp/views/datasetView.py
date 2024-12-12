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



@login_required(login_url='/login/')
def uploadView(request):
    return render(request, 'ENNApp/upload.html')

@login_required(login_url='/login/')
def addDataset(request):
    return redirect('listDatasets')

@login_required(login_url='/login/')
def listDatasets(request):

    context = {}

    return render(request, 'ENNApp/listDataset.html', context)


def convert_size(size_bytes):
    return "0 Bytes"



@login_required(login_url='/login/')
def deleteDataset(request, userName, fileName):
    return redirect('listDatasets')



@login_required(login_url='/login/')
def showDatasetSample(request, fileName, oldContext={}):
    context = {}

    return render(request, 'ENNApp/showDataset.html', context)


def loadContextMessages(request,context):
    del request.session['messageOk']
    
def preprocessDataset(request):
    context = {}

    return redirect('listDatasets')





def principalComponentAnalysis(request):
    context = {}

    return redirect('listDatasets')



@login_required(login_url='/login/')
def selectDataset(request):

    context = {}


    
    return render(request, 'ENNApp/selectDataSet.html', context)