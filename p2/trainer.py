from ast import parse
from itertools import product
from os import abort, error, path, rename, getcwd

from json import load
import argparse as _ap
from subprocess import run
from typing import Tuple

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# filename.net.combinations
# {
    # 'N1' : []
    # 'N2' : []
    # 'N3' : []
    # 'PTOT' : []
    # 'PR' : []
    # 'PTEST' : []
    # 'ITER' : []
    # 'ETA' : []
    # 'MOMENTUM' : []
# }

# Argumentos por parametro.
# WTS
# NERROR
# SEED
# CONTROL

# los parametros corresponden a:
# N1:     NEURONAS EN CAPA DE ENTRADA
# N2:     NEURONAS EN CAPA INTERMEDIA
# N3:     NEURONAS EN CAPA DE SALIDA
# PTOT:   cantidad TOTAL de patrones en el archivo .data
# PR:     cantidad de patrones de ENTRENAMIENTO
# PTEST:  cantidad de patrones de test (archivo .test)
# ITER:   Total de Iteraciones
# ETA:    learning rate
# u:      Momentum
# NERROR: graba error cada NERROR iteraciones
# WTS:    numero de archivo de sinapsis inicial
# SEED:   semilla para el rand()
# CONTROL:verbosity

# Comentarios:
# WTS=0 implica empezar la red con valores al azar
# cantidad de patrones de validacion: PTOT - PR
# SEED: -1: No mezclar los patrones: usar los primeros PR para entrenar y
#           el resto para validar.
#        0: Seleccionar semilla con el reloj, y mezclar los patrones.
#       >0: Usa el numero como semilla, y mezcla los patrones.
# verbosity: 0:resumen, 1:0 + pesos, 2:1 + datos

def shuffle(combinations: list, choices: str):
    if(choices == 'half'):
        return combinations

    if(choices == 'quarter'):
        return combinations

    return combinations
    
def createNetConfiguration(combination):
    return f'''{combination[0]}
{combination[1]}
{combination[2]}
{combination[3]}
{combination[4]}
{combination[5]}
{combination[6]}
{combination[7]}
{combination[8]}
{combination[9]}
{combination[10]}
0
0
0
'''

def getTrainData(rawdata: str):

    splitted = rawdata.splitlines()
    data_lns = list(filter(lambda x: x.startswith('#'), splitted))

    if(len(data_lns) == 0):
        abort()

    error_ln = list(filter(lambda x: x.startswith('#'), rawdata.splitlines()))[-1]

    return float(error_ln.split(':')[-1][:-1])

def main():
    
    parser = _ap.ArgumentParser('Trainer')
    parser.add_argument('filename', type=str)
    parser.add_argument('-c', '--choices', choices=['all', 'half', 'quarter'], default='all')
    parser.add_argument('-n', '--ntimes', type=int, default=10)
    
    args = parser.parse_args()
    # args.filename = 'ikeda/ikeda'

    # File names
    conf_filename = f'{args.filename}.net.combinations'
    temp_net_filename = f'{args.filename}.net'
    train_log_filename = f'{args.filename}.log'
    predict_net_filename = f'{args.filename}.predic'
    mse_net_filename = f'{args.filename}.mse'

    # Configuration & Log files.
    train_log = open(train_log_filename, 'w' if path.isfile(train_log_filename) else 'x')
    configurations_file = open(conf_filename, 'r')
    
    # Load configurations & generate combinations
    configurations = load(configurations_file)
    combinations = list(product(*list(configurations.values())))
    combinations  = shuffle(combinations, args.choices)
    
    # Logging
    train_log.write(f'Trained for {args.filename} started.\n')

    min_errors = []

    for i in range(len(combinations)):
        
        id = chr(65+(i%26)) * (int(i/26)+1)

        train_log.write(f'# Training net with configuration ID: {id}\n')
        train_log.write('# Configuration:\n')
        train_log.write(f'# {str(combinations[i])}\n')

        data = []

        # Create .net file, write conf and close it.
        temp_net_file = open(temp_net_filename, 'w' if path.isfile(temp_net_filename) else 'x')
        net_conf = createNetConfiguration(combinations[i])
        temp_net_file.write(net_conf)
        temp_net_file.close()

        printProgressBar(i*10, len(combinations)*10)

        for time in range(args.ntimes):
            
            train_res = run(f'./bpwd {args.filename}', shell=True, capture_output= True)

            if(train_res.returncode == 0):
                train_error = getTrainData(train_res.stdout.decode('ascii'))
                train_log.write(f'Error of train number: {time}: {train_error}\n')
                data.append(train_error)
                renameFile(predict_net_filename, f'{args.filename}_{id}_{time}.predic')
                renameFile(mse_net_filename, f'{args.filename}_{id}_{time}.mse')
            else:
                print(train_res.stdout.decode('ascii'))
                abort()
            
            printProgressBar(i*10+time, len(combinations)*10)


        avg =  sum(data) / args.ntimes

        differences = list(map(lambda x: abs(x - avg), data))
        
        closest_run =  differences.index(min(differences))

        train_log.write(f'Average error: {avg}\n')

        train_log.write(f'Train of minimum difference with AVG: {closest_run}')

        min_errors.append((id, avg))

    errors = list(map(lambda x: x[1],min_errors))

    min_err = min(errors)
    
    minn = error = min_errors[errors.index(min_err)]

    id, error = minn

    train_log.write(f'Minimum error: {error} at combination: {id}.')
    configurations_file.close()
    train_log.close()


def renameFile(fr, to):
    rename(fr'{getcwd()}/{fr}',fr'{getcwd()}/{to}')

if __name__ == '__main__':
    main()
