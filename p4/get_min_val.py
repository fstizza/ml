from sys import argv
from subprocess import run
from argparse import ArgumentParser


"""
Obtiene el K tal que minimiza el error de entrenamiento.
Dentro del rango dado.
"""

def getTrainTestErrors(lineList: list):
    lineListE = (list(filter(lambda x: 'Entrenamiento:' in x, lineList)))[0]
    lineListT = (list(filter(lambda x: 'Test:' in x, lineList)))[0]
    lineListV = (list(filter(lambda x: 'Validacion:' in x, lineList)))[0]
    resE = lineListE[14:18]
    resT = lineListT[5:10]
    resV = lineListV[11:15]
    return (float(resE),float(resT), float(resV))

def getMinimumK(fname: str, ran: list):

    stats = []
    for k in ran:
        with open(f'{fname}/{fname}.knn', 'r') as f:
            data = f.readlines()

        data[5] = f'{k}\n'

        with open(f'{fname}/{fname}.knn', 'w') as f:
            f.writelines(data)

        testValidacion = 0
        it = 10
        for n in range(it):
            res = run(f'./knn {fname}/{fname}', capture_output=True, shell=True)
            if (res.returncode != 0):
                print(f'FATAL ERROR: ./knn returned {res.returncode}')
                exit(1)
            (_, _, testV) = getTrainTestErrors(res.stdout.decode('ascii').splitlines())
            testValidacion += testV
        testValidacion /= it
        stats.append((k,testValidacion))

    minimum = min(stats, key = lambda t: t[1])
    print(f'The K that minimizes the Validation error is: {minimum[0]}')

def main():
    parser = ArgumentParser('Min K')
    parser.add_argument('name', type=str)
    args = parser.parse_args()
    getMinimumK(args.name, [2,3,4,5,7,9,10,12,13,18,21,27,30,34,37,40])

if __name__ == '__main__':
    main()
    
