import pandas as pd 
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
import sys
import json
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
# tensorflow
#import tensorflow
# keras
import keras
from keras.models import Sequential
from keras.layers import Dense
from .untils import readDataset, writeDataset, writeFile, createDirIfNotExist, readFile, writeFileWithJson, deleteFile

#from sklearn.model_selection import StratifiedKFold
#kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=5)



def executeDockerModel(models, rowData, datasetPath, userFolderPath):
    
    neuralNetworkFolderPath = os.path.join(userFolderPath, "neuralNetwork")
    modelFolderPath = os.path.join(userFolderPath, "model", "code")
    infoFolderPath = os.path.join(userFolderPath, "model", "info")

    for modelName in models:
        #Create model auto-generated code
        autoGeneratedCode = generateCode(models[modelName])
        codeModelName = str(modelName).removesuffix('.csv') + ".py"
        writeFile(autoGeneratedCode, modelFolderPath, codeModelName)
        
        #Create info File
        infoFileName = str(modelName).removesuffix('.csv') + ".info"
        writeFileWithJson(models[modelName], infoFolderPath, infoFileName)


def updateJson(jsonInfoTrainig, loss, epoch):
    jsonInfoTrainig["loss"]= loss
    jsonInfoTrainig["actualEpoch"]= epoch
    return json.dumps(jsonInfoTrainig)


def executeModel(models, rowData, datasetPath, userFolderPath):

    neuralNetworkFolderPath = os.path.join(userFolderPath, "neuralNetwork")
    modelFolderPath = os.path.join(userFolderPath, "model", "code")
    infoFolderPath = os.path.join(userFolderPath, "model", "info")

    toRet = {}
    dataframe = readDataset(datasetPath)

    X = dataframe[rowData["dataNames"]].values
    Y = dataframe[rowData["targetsNames"]].values
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

    #Initialize Info Files
    for modelName in models:
        #Callbacks
            jsonInfoTrainig = {
                "maxEpoch": models[modelName]["epochs"],
                "actualEpoch": 0,
                "loss": "Not Obtained", 
                "name": str(modelName),
                #"userOwner": request.user.username
            }

            writeFile(json.dumps(jsonInfoTrainig), infoFolderPath, str(modelName)+ ".temp")

    for modelName in models:
        try:
            
            #Clear Sesion
            keras.backend.clear_session()

            #Create the secuential model
            model = Sequential()

            #Imput Layer
            dimNumber = int(models[modelName]["firstDimNumber"])
            activation = str(models[modelName]["firstActivation"])
            model.add(Dense(dimNumber, activation=activation,input_dim=dimNumber))
            
            #Hidden Layers
            for hidenLayer in models[modelName]["hidenLayers"]:
                dimNumber = int(models[modelName]["hidenLayers"][hidenLayer]["dimNumber"])
                activation = str(models[modelName]["hidenLayers"][hidenLayer]["activation"])
                model.add(Dense(dimNumber, activation=activation))
            
            #Output Layer
            dimNumber = int(models[modelName]["lastDimNumber"])
            activation = str(models[modelName]["lastActivation"])
            model.add(Dense(dimNumber, activation=activation))

            #Compile the model
            lossFuntion = str(models[modelName]["lossFuntion"])
            optimicer = str(models[modelName]["optimicer"])
            model.compile(loss=lossFuntion, optimizer=optimicer)

            #Callbacks
            jsonInfoTrainig = {
                "maxEpoch": models[modelName]["epochs"],
                "actualEpoch": 0,
                "loss": "Not Obtained", 
                "name": str(modelName),
                #"userOwner": request.user.username
            }
            logger = keras.callbacks.LambdaCallback(
                on_epoch_end=lambda epochs,logs: writeFile(str(updateJson(jsonInfoTrainig, logs["loss"], epochs)), infoFolderPath, str(modelName)+ ".temp"),  
                on_train_end=lambda logs: deleteFile(infoFolderPath, str(modelName)+ ".temp"))


            #Fit the model whith the train data (and indicate the numer of iterations for the data)
            epochs = int(models[modelName]["epochs"])
            batchSize = int(models[modelName]["batchSize"])
            model.fit(X_train, y_train, epochs=epochs, batch_size=batchSize, callbacks=[logger])
            
            #Model summary
            print(model.summary())

            # evaluate the model
            lossVal = model.evaluate(X_test, y_test, verbose=0)
            models[modelName]["lossVal"] = {
                "value": lossVal,
                "metric": lossFuntion
            }
            print(lossVal)

            #Store data and target names
            models[modelName]["dataNames"] = rowData["dataNames"]
            models[modelName]["targetsNames"] = rowData["targetsNames"]
            
            #Create model auto-generated code
            autoGeneratedCode = generateCode(models[modelName])
            codeModelName = str(modelName).removesuffix('.csv') + ".py"
            writeFile(autoGeneratedCode, modelFolderPath, codeModelName)
            
            #Create NeuralNetwork File
            neuralNetworkName = str(modelName).removesuffix('.csv') + ".keras"
            createDirIfNotExist(neuralNetworkFolderPath)
            neuralNetworkPath = os.path.join(neuralNetworkFolderPath, neuralNetworkName)
            model.save(neuralNetworkPath)

            #Create info File
            infoFileName = str(modelName).removesuffix('.csv') + ".info"
            writeFileWithJson(models[modelName], infoFolderPath, infoFileName)
            

        except BaseException as e:
            print("Error -> " + str(e))
            if toRet["messageErr"] is not None:
                toRet.update({"messageErr": "An error occurred in Model " + modelName})
            else:
                toRet.update({"messageErr": toRet["messageErr"] + ", " + modelName})
    
    return toRet
    
 

def generateCode(model):
    code = ""
    code += '#------------------------------------------------------------------------------\n'
    code += '# <auto-generated>\n'
    code += '#     This code was generated by Easy Neural Network\n'
    code += '#     Runtime Version:1.0\n'
    code += '#\n'
    code += '#     Changes to this file may cause incorrect behavior and will be lost if\n'
    code += '#     the code is regenerated.\n'
    code += '# </auto-generated>\n'
    code += '#------------------------------------------------------------------------------\n'
    code += '\n'
    code += '\n'
    code += '# pandas\n'
    code += 'import pandas as pd \n'
    code += '# numpy\n'
    code += 'import numpy as np\n'
    code += '# sklearn\n'
    code += 'from sklearn.preprocessing import StandardScaler, MinMaxScaler\n'
    code += 'from sklearn.model_selection import train_test_split\n'
    code += '# tensorflow\n'
    code += 'import tensorflow\n'
    code += '# keras\n'
    code += 'import keras\n'
    code += 'from keras.models import Sequential\n'
    code += 'from keras.layers import Dense\n'
    code += '\n'
    code += '\n'

    code += 'def generateNeuralNetwork(trainData,trainTarget):\n'
    code += '    #Clear Sesion\n'
    code += '    keras.backend.clear_session()\n'
    code += '\n'
    code += '    #Create the secuential model\n'
    code += '    model = Sequential()\n'
    code += '\n'
    code += '    #Imput Layer\n'
    code += '    dimNumber = int(' + str(model["firstDimNumber"]) + ')\n'
    code += '    activation = "' + str(model["firstActivation"]) + '" \n'
    code += '    model.add(Dense(dimNumber, activation=activation,input_dim=dimNumber))\n'
    for hidenLayer in model["hidenLayers"]:
        code += '    \n'
        code += '    #Hidden Layer ' + hidenLayer + '\n'
        code += '    dimNumber = int('+ str(model["hidenLayers"][hidenLayer]["dimNumber"]) +')\n'
        code += '    activation = str("'+ str(model["hidenLayers"][hidenLayer]["activation"])+'")\n'
        code += '    model.add(Dense(dimNumber, activation=activation))\n'
    code += '    \n'
    code += '    #Output Layer\n'
    code += '    dimNumber = int('+ str(model["lastDimNumber"]) + ')\n'
    code += '    activation = str("'+ str(model["lastActivation"])+ '")\n'
    code += '    model.add(Dense(dimNumber, activation=activation))\n'
    code += '\n'
    code += '    #Compile the model\n'
    code += '    lossFuntion = str("'+ str(model["lossFuntion"])+ '")\n'
    code += '    optimicer = str("'+ str(model["optimicer"])+ '")\n'
    code += '    model.compile(loss=lossFuntion, optimizer=optimicer)\n'
    code += '\n'
    code += '\n'
    code += '    #Fit the model whith the train data (and indicate the numer of iterations for the data)\n'
    code += '    epochs = int('+ str(model["epochs"]) + ')\n'
    code += '    batchSize = int('+ str(model["batchSize"]) + ')\n'
    code += '    model.fit(trainData, trainTarget, epochs=epochs, batch_size=batchSize)\n'
    code += '    \n'
    code += '    #Model summary\n'
    code += '    print(model.summary())\n'

    return code


def readInfoFile(filePath):
    content = readFile(filePath)

    return content




def loadNeuralNetworkFile(userName, fileName):
        
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        filePath = os.path.join(BASE_DIR, "userFiles", userName + "/neuralNetwork/" + fileName)
        infoFolderPath = os.path.join(BASE_DIR, "userFiles", userName , "model", "info")
        
        infoFileName = str(fileName).removesuffix('.keras') + ".info"

        model = keras.saving.load_model(filePath)

        modelConfig = model.get_config()

        layers = modelConfig["layers"]



        modelInfoJson = {
            "batchSize": "Unknown",
            "epochs": "Unknown",
            "lossFuntion": "Unknown",
            "lossVal": "Unknown",
            "modelName": str(fileName).removesuffix('.keras'),
            "optimicer": "Unknown"
        }

        hiddenLayers = {}
        isFirstLayer = True
        hiddenIndexLayer = 0

        for layer in layers:
            if "config" in layer and "activation" in  layer["config"] and "units" in layer["config"]:
                if(isFirstLayer):
                        isFirstLayer = False
                        modelInfoJson["firstActivation"] = layer["config"]["activation"]
                        modelInfoJson["firstDimNumber"] = layer["config"]["units"]
                else:
                    indexLayer = layers.index(layer)
                    if indexLayer < len(layers) -1:
                        hiddenIndexLayer += 1 
                        hiddenLayers[hiddenIndexLayer] = {
                                "activation": layer["config"]["activation"], 
                                "dimNumber": layer["config"]["units"]
                            }
                    else:
                        modelInfoJson["lastActivation"] = layer["config"]["activation"]
                        modelInfoJson["lastDimNumber"] = layer["config"]["units"]
        modelInfoJson["hidenLayers"] = hiddenLayers
        
        print(modelInfoJson)
        writeFileWithJson(modelInfoJson, infoFolderPath, infoFileName)



def evaluate(data, neuralNetworkPath, datasetPath, metricName, rowData):
    #Load dataset
    dataframe = readDataset(datasetPath)

    X_True = dataframe[rowData["dataNames"]].values
    Y_True = dataframe[rowData["targetsNames"]].values

    #Load Model
    model = keras.saving.load_model(neuralNetworkPath, custom_objects=None, compile=True, safe_mode=True)


    #Evaluate Loss
    lossVal = model.evaluate(X_True, Y_True)
    data["lossVal"] = {
        "value": lossVal,
        "metric": model.loss
    }

    #Metrics
    if metricName == "mean_squared_error":
        metric = keras.metrics.MeanSquaredError()

    if metricName == "root_mean_squared_error":
        metric = keras.metrics.RootMeanSquaredError()
    
    if metricName == "mean_absolute_error":
        metric = keras.metrics.MeanAbsoluteError()

    if metricName == "mean_absolute_percentage_error":
        metric = keras.metrics.MeanAbsolutePercentageError()

    if metricName == "mean_squared_logarithmic_error":
        metric = keras.metrics.MeanSquaredLogarithmicError()

    if metricName == "cosine_similarity":
        metric = keras.metrics.CosineSimilarity()

    if metricName == "logcosh":
        metric = keras.metrics.LogCoshError()

    if metricName == "r2_score":
        metric = keras.metrics.R2Score()
        
    
    Y_Result = model.predict(X_True)
    metric.update_state(Y_True, Y_Result)
    scoreTensor = metric.result()
    scoreValue = np.array(scoreTensor)

    if "metrics" not in data:
        data["metrics"] = {}
    
    data["metrics"][str(metricName)] = str(scoreValue)

    return data