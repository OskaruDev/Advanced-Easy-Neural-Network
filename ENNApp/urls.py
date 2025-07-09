from django.urls import path
#from . import views
from .views import userView
from .views import datasetView
from .views import neuralNetworkView
from .views import evaluateModelView
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.auth import views as auth_views


urlpatterns = [
    #path('testForm', views.testForm, name='testForm'),
    #path('<int:question_id>/', views.detail, name='detail'),
    #path('testPost/', views.testPost, name='testPost'),
    #------------------------------------------------------
    path('', userView.index),
    path('index/', userView.index, name='index'),
    path('uploadDatasetView/', datasetView.uploadDatasetView, name='uploadDatasetView'),
    path('addDataset/', datasetView.addDataset, name='addDataset'),
    path('listDatasets/', datasetView.listDatasets, name='listDatasets'),
    path('showDatasetSample/<str:fileName>/', datasetView.showDatasetSample, name='showDatasetSample'),
    path('deleteDataset/<str:userName>/<str:fileName>/', datasetView.deleteDataset, name='deleteDataset'),
    path('preprocessDataset/', datasetView.preprocessDataset, name='preprocessDataset'),
    path('principalComponentAnalysis/', datasetView.principalComponentAnalysis, name='principalComponentAnalysis'),
    path('selectDataset/', datasetView.selectDataset, name='selectDataset'),
    path('listNeuralNetwork/', neuralNetworkView.listNeuralNetwork, name='listNeuralNetwork'),
    path('listTrainingNeuralNetwork/', neuralNetworkView.listTrainingNeuralNetwork, name='listTrainingNeuralNetwork'),
    path('deleteNeuralNetwork/<str:userName>/<str:fileName>/', neuralNetworkView.deleteNeuralNetwork, name='deleteNeuralNetwork'),
    path('createModel/<str:fileName>/', neuralNetworkView.createModel, name='createModel'),
    path('executeModel/', neuralNetworkView.executeModel, name='executeModel'),
    path('detailNeuralNetwork/<str:fileName>/', neuralNetworkView.detailNeuralNetwork, name='detailNeuralNetwork'),
    path('addNeuralNetwork/', neuralNetworkView.addNeuralNetwork, name='addNeuralNetwork'),
    path('uploadNeuralNetworkView/', neuralNetworkView.uploadNeuralNetworkView, name='uploadNeuralNetworkView'),
    path('listEvaluationView/', evaluateModelView.listEvaluationView, name='listEvaluationView'),
    path('evaluateNeuralNetwork/<str:fileName>/', evaluateModelView.evaluateDetailNeuralNetwork, name='evaluateDetailNeuralNetwork'),
    path('evaluateModel/', evaluateModelView.evaluateModel, name='evaluateModel'),
    path('selectTargetModal/', evaluateModelView.selectTargetModal, name='selectTargetModal'),
    path('login/', userView.loginUser, name='login'),
    path('logout/', userView.logoutUser, name='logout'),
    path('register/', userView.registerUser, name='register'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)