import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from json import load

def getTreeStats(fname: str, data: str):
    stats_file = open(fname)
    stats = load(stats_file)
    stats_file.close
    return list(map(lambda x: x[data],stats))

def getData(fname):
    fileHandle = open ( fname,"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    lineList = list(filter(lambda x: '<<' in x, lineList))

    trainingError = float((list(map(lambda x: x.replace('%', ''), re.findall(r'(?<=\()[^)]*(?=\))', lineList[0]))))[1])
    testError =  float((list(map(lambda x: x.replace('%', ''), re.findall(r'(?<=\()[^)]*(?=\))', lineList[1]))))[1])
    return (trainingError, testError)


def getDataNb(fname):
    fileHandle = open ( fname,"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    lineListE = (list(filter(lambda x: 'Entrenamiento:' in x, lineList)))[0]
    lineListT = (list(filter(lambda x: 'Test:' in x, lineList)))[0]
   # print(list(filter(lambda x: 'Test:' in x, lineList)))
    resE = lineListE[14:18]
    resT = lineListT[5:10]
    return (float(resE),float(resT))

def main():
    avgTnError =    []
    avgTsError    = []
    avgTnErrorP   = []
    avgTsErrorP   = []
    nnTrainError  = []
    nnTestError   = []
    nnTrainErrorP = []
    nnTestErrorP  = []
    nbTrainError  = []
    nbTestError   = []
    nbTrainErrorP = []
    nbTestErrorP  = []
    numbers = ['2', '4', '8', '16', '32']
    mse_headers = ['mse_train_stoc', 'mse_train', 'mse_val',
               'mse_test', 'clas_train', 'clas_val', 'clas_test', 'line']
    
    avgTnError  = getTreeStats('stats_diagonal','tr_ap_error')
    avgTsError  = getTreeStats('stats_diagonal','tt_ap_error')
    avgTnErrorP = getTreeStats('stats_parallel','tr_ap_error')
    avgTsErrorP = getTreeStats('stats_parallel','tt_ap_error')

    for j in numbers:
        pdf = pd.read_csv('nn/'+j+'/parallel.mse',sep='\s+', header=None, names=mse_headers)
        ddf = pd.read_csv('nn/'+j+'/diagonal.mse',sep='\s+', header=None, names=mse_headers)
        nnTrainError.append(ddf['clas_train'].mean()*100)
        nnTestError.append(ddf['clas_test'].mean()*100)
        nnTrainErrorP.append(pdf['clas_train'].mean()*100)
        nnTestErrorP.append(pdf['clas_test'].mean()*100)
        (resED,resTD) = getDataNb('nb/'+j+'/diagonal.dt')
        (resEP,resTP) = getDataNb('nb/'+j+'/parallel.dt')
        nbTrainError.append(resED)
        nbTestError.append(resTD)
        nbTrainErrorP.append(resEP)
        nbTestErrorP.append(resTP)

    numbersi = list(map(int,numbers))
    errors = pd.DataFrame({
        'tree-diag-train' : avgTnError,
        'tree-diag-test'  : avgTsError,
        'tree-par-train'  : avgTnErrorP,
        'tree-par-test'   : avgTsErrorP,
        'nn-diag-train'   : nnTrainError,
        'nn-diag-test'    : nnTestError,
        'nn-par-train'    : nnTrainErrorP,
        'nn-par-test'     : nnTestErrorP,
        'bayes-diag-train': nbTrainError,
        'bayes-diag-test' : nbTestError,
        'bayes-par-train' : nbTrainErrorP,
        'bayes-par-test'  : nbTestErrorP,
    }, index= numbersi)
    ax = errors.plot(title='Errores', style=[ '--*', '^--','v--','s--','|-', '-', ',-','p-','-','-','-','-'], color=["green","violet", "red", "blue","green","violet", "red", "blue","green", "violet", "red", "blue"], xticks=numbersi)
    ax.set_xlabel('Dimension')
    ax.set_ylabel('Error porcentual')

    plt.savefig('grafico.jpg')
    plt.show()


if __name__ == '__main__':
    main()