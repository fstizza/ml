import pandas as pd
import re
import matplotlib.pyplot as plt
import argparse as ap



def main():
    argparser = ap.ArgumentParser('Plt')
    argparser.add_argument('id', type=str)
    args = argparser.parse_args()

    colNames = ["C1","MseTrain","MseValid","MseTest","C5","C6","C7"]

    data = pd.read_csv(f'ikeda_{args.id}.mse', sep="	", header = 0, names = colNames)

    mseTrain = data["MseTrain"].tolist()
    mseValid = data["MseValid"].tolist()
    mseTest = data["MseTest"].tolist()
    
    err = data[["MseTrain","MseValid","MseTest"]]

    ax = err.plot(title='Errores', color=["green", "blue", "red"]) #xticks
    ax.set_xlabel('Epoca')
    ax.set_ylabel('Mse')
    # plt.show()
    
    plt.savefig(f'ikeda_plot_{args.id}.jpeg')
    

if __name__ == '__main__':
    main()