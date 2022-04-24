from sys import argv
from matplotlib import pyplot as plt
import pandas as pd

def main():
    predic_headers = ['x', 'y', 'class']
    ddf = pd.read_csv(f'{argv[1]}.predic.d',sep='\s+', header=None, names=predic_headers)
    c0 = ddf.loc[ddf['class'] == 0]
    c1 = ddf.loc[ddf['class'] == 1]

    c0x = c0['x']
    c0y = c0['y']

    c1x = c1['x']
    c1y = c1['y']

    plt.scatter(c0x, c0y)
    plt.scatter(c1x, c1y)
    plt.show()

if __name__ == '__main__':
    main()
    
