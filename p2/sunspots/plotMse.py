import pandas as pd
import re
import matplotlib.pyplot as plt
import argparse as ap

def main(id: str):
    colNames = ["C1","MseTrain","MseValid","MseTest","C5","C6","C7", "Decay"]
    data = pd.read_csv(f'ssp_{id}.mse', sep="	", header = 0, names = colNames)
    err = data[["MseTrain","MseValid","MseTest"]]
    ax = err.plot(title='Errores', color=["green", "blue", "red"]) #xticks
    ax.set_xlabel('Epoca')
    ax.set_ylabel('Mse')
    plt.savefig(f'ssp_{id}.jpeg')
    

def main2(id: str):
    colNames = ["C1","MseTrain","MseValid","MseTest","C5","C6","C7", "Decay"]
    data = pd.read_csv(f'ssp_{id}.mse', sep="	", header = 0, names = colNames)
    err = data[["Decay"]]
    plt.title('Penalización')
    plt.scatter(range(len(data)), err)
    plt.savefig(f'wd_ssp_{id}.jpeg')



if __name__ == '__main__':
    argparser = ap.ArgumentParser('Plt')
    argparser.add_argument('id', type=str)
    argparser.add_argument('-w','--wd', action='store_true')
    args = argparser.parse_args()
    if(args.wd):
        main2(args.id)
    else:
        main(args.id)
