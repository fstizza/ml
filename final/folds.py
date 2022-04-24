from json import load
import os
from numpy import floor, sqrt
import pandas as pd
from pandas.core.frame import DataFrame
from sklearn import svm
import sklearn
from sklearn.metrics import accuracy_score
from itertools import product
import re
import numpy as np
from statistics import mean
# Method types:
SVM = 'SVM'
NB  = 'NB'
DT  = 'DT'

def sortByClass(dataframe: DataFrame, classes: list):
    '''

    '''
    res = []
    _, classColId = dataframe.shape
    for c in classes:
        res.append(dataframe[dataframe.iloc[:,classColId-1] == c])
    return res

def foldByClass(k: int, data: list):
    '''
        int k ; cantidad de folds
        List<List<num>> data ; lista de datos ordenadas por clase.
    '''
    res = []
    for c in data:
        l = len(c) 
        if(l < k):
            raise Exception('Cant fold if data length is lower than the k folds.')
        count = int(floor(l / k))
        remaining = l % k
        folds = list(map(lambda x: c[x*count:count*(x+1)], range(k)))
        for i in range(remaining):
            folds[i] = folds[i].append(c.iloc[count * k + i,:])
        res.append(folds)
    return res

def getData(name: str):
    '''
        Reads data from a CSV named: name'
    '''
    cols = list(map(str,range(0,103)))
    ddf = pd.read_csv(name,sep=',', header=0, names=cols)
    return ddf

def splitDataFromTargets(ddf: DataFrame): 
    samples, features = ddf.shape
    data = ddf.iloc[0:samples, 0:features-1]
    targets = ddf.iloc[0:samples, features-1]
    return (data, targets)

def prepareData(name: str, k: int, classes: list):
    data = getData(f'{name}.data')
    sorted = sortByClass(data, classes)
    return foldByClass(k, sorted)

def getTrainTestData(data, testFold: int, validationFold: bool = False):
    train = pd.DataFrame()
    test = pd.DataFrame()
    validation = pd.DataFrame()

    for c in data:
        trainFolds = list(range(len(c)))
        trainFolds.remove(testFold)
        test = test.append(c[testFold])
        if(validationFold):
            trainFolds.remove((testFold+1) % len(c))
            validation = validation.append(c[(testFold+1) % len(c)])

        for i in trainFolds:
            train = train.append(c[i])

    return (train, test, validation)

def trainSVM(name: str, data, kfolds: int, kernel: str, optimizable_params: dict):
    tr, tt, tv = getTrainTestData(data, 0, True)
    min_error = 101

    values = []
    if(len(list(optimizable_params.values())) > 1):
        values = list(product(*optimizable_params.values()))
    elif(len(optimizable_params.values())):
        values = list(map(lambda x: [x],list(optimizable_params.values())[0]))

    val = values[0]
    for c in values:
        args = getArgsFromValues(c, optimizable_params.keys())
        args['kernel'] = kernel
        (_, tt_error, cl) = train(name, SVM, tr, tv, args)
        tt2, tt_tgt = splitDataFromTargets(tt)
        t2_error = 1 - accuracy_score(tt_tgt.values, cl.predict(tt2.values))
        err = mean([tt_error, t2_error])    
        if(err < min_error):
            val = c
            min_error = err
    
    print(f'Optimized SVM values: {val} for kernel: {kernel}')
    args = getArgsFromValues(c, optimizable_params.keys())
    args['kernel'] = kernel
    return doTrain(name, SVM, data, kfolds, args)

def getArgsFromValues(values, keys):
    keys = list(keys)
    arg = {}
    for k in range(len(keys)):
        arg[keys[k]] = values[k]
    return arg

def doTrain(name:str, method:str, data, kfolds: int, arguments: dict = None):
    tt_errors = []
    for k in range(kfolds):
        tr, tt, _ = getTrainTestData(data, k)
        _, tt_error, _ = train(name, method, tr, tt, arguments)
        tt_errors.append(tt_error)
    return tt_errors

def getMeasures(errors: list):
    mu = sum(errors) / len(errors)
    sd = sqrt(sum(map(lambda x: (x - mu)**2, errors)) / (len(errors) - 1))
    return (mu, sd)

def t_test(errors1, errors2):
    diff = list(map(lambda x: errors1[x] - errors2[x], range(len(errors1))))
    d, sd = getMeasures(diff)
    return d / (sd / sqrt(len(errors1)))

def train(name: str, method: str, train, test, arguments: map = None):
    tr_error = None
    tt_error = None

    if(method == SVM):
        cls = None
        if(arguments['kernel'] == 'rbf'):
            cls = svm.SVC(C=arguments['C'], kernel='rbf', gamma=arguments['G'])
        else:
            cls = svm.SVC(C=arguments['C'], kernel='linear',tol=0.1)
        tr, tr_tgt = splitDataFromTargets(train)
        tt, tt_tgt = splitDataFromTargets(test)
        
        cls.fit(tr.values, tr_tgt.values)
        tr_error = 1 - accuracy_score(tr_tgt.values, cls.predict(tr.values))
        tt_error = 1 - accuracy_score(tt_tgt.values, cls.predict(tt.values))
        return (tr_error, tt_error, cls)
    elif(method == NB):
        # Train
        setNbData(name, train, test)
        os.system(f'./nb NB/{name} > ./NB/{name}.dt')
        tr_error, tt_error = getNbData(f'./NB/{name}.dt')
    elif(method == DT):
        setDtData(name, train, test)
        os.system(f'c4.5 -f ./DT/{name} -u > ./DT/{name}.dt')
        tr_error, tt_error = getDtData(f'./DT/{name}.dt')
    else:
        raise Exception('Undefined method')
    
    return (tr_error, tt_error, None)

def setNbData(name, train, test):
    with open(f'./NB/{name}.nb', 'r') as f:
        data = f.readlines()
        data[2] = f'{len(train)}\n'
        data[3] = f'{len(train)}\n' 
        data[4] = f'{len(test)}\n' 
    with open(f'./NB/{name}.nb', 'w') as f:
        f.writelines(data)
    writeTrainTestData(f'./NB/{name}', train, test)

def getNbData(fname):
    fileHandle = open (fname, "r")
    lineList = fileHandle.readlines()
    fileHandle.close()
    lineListE = (list(filter(lambda x: 'Entrenamiento:' in x, lineList)))[0]
    lineListT = (list(filter(lambda x: 'Test:' in x, lineList)))[0]
    resE = lineListE[14:18]
    resT = lineListT[5:10]
    return (float(resE),float(resT))

def setDtData(name: str, train: DataFrame, test: DataFrame):
    writeTrainTestData(f'./DT/{name}', train, test)

def getDtData(fname):
    fileHandle = open(fname, "r")
    lineList = fileHandle.readlines()
    fileHandle.close()
    lineList = list(filter(lambda x: '<<' in x, lineList))
    trainingError = float((list(map(lambda x: x.replace('%', ''), re.findall(r'(?<=\()[^)]*(?=\))', lineList[0]))))[1])
    testError =  float((list(map(lambda x: x.replace('%', ''), re.findall(r'(?<=\()[^)]*(?=\))', lineList[1]))))[1])
    return (trainingError, testError)

def writeTrainTestData(name: str, train: DataFrame, test: DataFrame):
    train = train.astype({'102':int})
    train_file = open(f'{name}.data', 'w' if os.path.isfile(f'{name}.data') else 'x')
    train.to_csv(train_file, header=False, index=False)
    train_file.close()

    test = test.astype({'102':int})
    test_file = open(f'{name}.test', 'w' if os.path.isfile(f'{name}.test') else 'x')
    test.to_csv(test_file, header=False, index=False)
    test_file.close()
  
def validateData(data: list):
    for c in data:
        for k in range(len(c)):
            lista = list(range(len(c)))
            lista.remove(k)
            for l in lista:
                if(list(pd.merge(c[k], c[l]).values) != []):
                    raise Exception('FUCK!')

def main():
    os.chdir('ej1')
    kfolds = 10
    name = 'BBBs'
    data = prepareData(name, kfolds, [0,1])
    c = [10 ** x  for x in range(-5, 5)]
    c2 = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    g = [x * 0.1 for x in range(1,10)]
    # dt_error = doTrain(name, DT, data, kfolds)
    # nb_error = doTrain(name, NB, data, kfolds)
    svm_nonlineal_error = trainSVM(name, data, kfolds, 'rbf', {'C': c2, 'G': g})
    # svm_lineal_error = trainSVM(name, data, kfolds, 'linear', {'C': c})
    # svm2 = [0.23809523809523814,0.30952380952380953,0.2857142857142857,0.2857142857142857,0.3571428571428571,0.2195121951219512,0.24390243902439024,0.24390243902439024,0.29268292682926833,0.25]
    # dt_error = list(map(lambda x: x/100.0, [23.8, 33.3, 19.0, 40.5, 35.7, 24.4, 26.8, 26.8, 24.4, 20.0]))
    # nb_error = list(map(lambda x: x/100.0, [35.71, 38.09, 35.71, 40.47, 45.23, 65.85, 39.02, 34.14, 41.46, 50.0]))
    # svm_nonlineal_error = [0.26190476190476186, 0.23809523809523814, 0.30952380952380953, 0.23809523809523814, 0.33333333333333337, 0.14634146341463417, 0.29268292682926833, 0.29268292682926833, 0.29268292682926833, 0.25]
    # svm_lineal_error = [0.33333333333333337, 0.30952380952380953, 0.2857142857142857, 0.33333333333333337, 0.40476190476190477, 0.31707317073170727, 0.29268292682926833, 0.24390243902439024, 0.2682926829268293, 0.275]
    
    print(svm_nonlineal_error)
    # print(svm_lineal_error)
    # print(getMeasures(dt_error))
    # print(getMeasures(nb_error))
    print(getMeasures(svm_nonlineal_error))
    # print(getMeasures(svm_lineal_error))
    # print(f'Error entre 1° y 2°: {t_test(dt_error, svm_nonlineal_error)}')
    # print(f'Error entre 1° y 4°: {t_test(nb_error, svm_nonlineal_error)}')

def printMeasure(v):
    mu, sd = v
    print(f'Error medio de test: {mu} - Desvío estándar: {sd}')

if __name__ == '__main__':
    main()

# Clase1 ; Clase2 ; ... ; ClaseN
#Optimized SVM values: (100, 0.1) for kernel: rbf
#Optimized SVM values: [10000] for kernel: linear

#  Optimized SVM values: (100, 0.1) for kernel: rbf
# Optimized SVM values: [10000] for kernel: linear
# dt_error = [23.8, 33.3, 19.0, 40.5, 35.7, 24.4, 26.8, 26.8, 24.4, 20.0]
# nb_error = [35.71, 38.09, 35.71, 40.47, 45.23, 65.85, 39.02, 34.14, 41.46, 50.0]
# svm_nonlineal_error = [0.26190476190476186, 0.23809523809523814, 0.30952380952380953, 0.23809523809523814, 0.33333333333333337, 0.14634146341463417, 0.29268292682926833, 0.29268292682926833, 0.29268292682926833, 0.25]
# svm_lineal_error = [0.33333333333333337, 0.30952380952380953, 0.2857142857142857, 0.33333333333333337, 0.40476190476190477, 0.31707317073170727, 0.29268292682926833, 0.24390243902439024, 0.2682926829268293, 0.275]

# Optimized SVM values: (10, 0.1) for kernel: rbf
# Optimized SVM values: [100] for kernel: linear 

#[0.23809523809523814, 0.30952380952380953, 0.2857142857142857, 0.2857142857142857, 0.3571428571428571, 0.2195121951219512, 0.24390243902439024, 0.24390243902439024, 0.29268292682926833, 0.25]
#[0.33333333333333337, 0.30952380952380953, 0.2857142857142857, 0.33333333333333337, 0.40476190476190477, 0.31707317073170727, 0.29268292682926833, 0.24390243902439024, 0.2682926829268293, 0.275]
