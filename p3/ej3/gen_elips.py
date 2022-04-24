#!/usr/bin/python

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

etas = [0.5, 0.1, 0.05, 0.01, 0.001]
momentums = [0.75]
mse_headers = ['mse_train_stoc', 'mse_train', 'mse_val',
               'mse_test', 'clas_train', 'clas_val', 'clas_test', 'line']
bins = [8, 16, 32, 64, 128, 256]

def train_parameter(prefix1, arr1, prefix2, arr2, line_in_file1, line_in_file2):
    # errors
    for elem1 in arr1:
        for elem2 in arr2:
            filePrefix = f'{prefix1}_{elem1}_{prefix2}_{elem2}'
            fname = f'{filePrefix}_dos_elipses'

            os.system(f'mkdir datasets/{filePrefix}')
            os.system(f'rm datasets/{filePrefix}/*')
            os.system(
                f'cp datasets/dos_elipses.data datasets/{filePrefix}/{fname}.data')
            os.system(
                f'cp datasets/dos_elipses.net datasets/{filePrefix}/{fname}.net')
            os.system(
                f'cp datasets/dos_elipses.test datasets/{filePrefix}/{fname}.test')

            with open(f'datasets/{filePrefix}/{fname}.net', 'r') as f:
                data = f.readlines()

            data[line_in_file1] = f'{elem1}\n'
            data[line_in_file2] = f'{elem2}\n'

            with open(f'datasets/{filePrefix}/{fname}.net', 'w') as f:
                f.writelines(data)

            print(f'./../../bin/bp datasets/{filePrefix}/{fname}')
            os.system(f'./../../bin/bp datasets/{filePrefix}/{fname}')
            os.system(f'./../../bin/discretiza datasets/{filePrefix}/{fname}')

            # """print predictions"""
            data = pd.read_csv(f'datasets/{filePrefix}/{fname}.predic.d',  header=None,
                               names=['X', 'Y', 'clase'], sep='\s+')

            ax = data[data['clase'] == 0].plot.scatter(figsize=(
                7.5, 7.5), x='X', y='Y', alpha=0.5, label='0', facecolors='none', edgecolors='#0cc70c', c='none')
            data[data['clase'] == 1].plot.scatter(
                x='X', y='Y', alpha=0.5, label='1', ax=ax, facecolors='none', edgecolors='#d40000', c='none')
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.2, 1.2)

            plt.axhline(0, color='black', alpha=0.35)
            plt.axvline(0, color='black', alpha=0.35)
            plt.savefig(
                f'../img/{prefix1}_{elem1}_{prefix2}_{elem2}_dos_elipses.png')
            plt.close()

            # """print errors"""
            df = pd.read_csv(f'datasets/{filePrefix}/{fname}.mse',
                             sep='\s+', header=None, names=mse_headers)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            # ax.plot(range(200, 40001, 200), df['clas_train'], alpha=0.5, label='mse_train', color='#0cc70c')
            # ax.plot(range(200, 40001, 200), df['clas_val'], alpha=0.5, label='mse_val', color='#0000ff')
            # ax.plot(range(200, 40001, 200), df['clas_test'], alpha=0.5, label='mse_test', color='#d40000')
            ax.plot(range(200, 40001, 200), df['mse_train'], alpha=0.5,
                    label='mse_train', color='#0cc70c')
            ax.plot(range(200, 40001, 200), df['mse_val'], alpha=0.5,
                    label='mse_val', color='#0000ff')
            ax.plot(range(200, 40001, 200), df['mse_test'], alpha=0.5,
                    label='mse_test', color='#d40000')

            ax.set_xlabel('Epocas')
            ax.set_ylabel('Error')
            plt.title(f'{prefix1}_{elem1}_{prefix2}_{elem2}_dos_elipses')
            plt.legend()
            plt.savefig(f'../img/{prefix1}_{elem1}_{prefix2}_{elem2}.png')

            plt.close()


def get_error_number(evaluation_results):
    return list(map(lambda x: x.replace('%', ''), re.findall(r'[\d]+.[\d]+', evaluation_results)))[0]


def nb_train_parameter(prefix):
    # errors
    train_err = []
    test_err = []
    val_err = []
    for bin in bins:
        fname = f'{prefix}_{bin}_doselipses'
        os.system(f'cp ./datasets/doselipses.data ./datasets/{prefix}/{fname}.data')

        os.system(f'cp ./datasets/synth2.nb2 ./datasets/{prefix}/{fname}.nb2')

        os.system(f'cp ./datasets/doselipses.test ./datasets/{prefix}/{fname}.test')

        with open(f'datasets/{prefix}/{fname}.nb2', 'r') as f:
            data = f.readlines()

        data[5] = f'{bin}\n'

        with open(f'datasets/{prefix}/{fname}.nb2', 'w') as f:
            f.writelines(data)

        print(f'./nb2 datasets/{prefix}/{fname}')
        os.system(
            f'./nb2 datasets/{prefix}/{fname} > datasets/{prefix}/{fname}.out')
        data = pd.read_csv(f'datasets/{prefix}/{fname}.predic',  header=None,
                           names=['X', 'Y', 'clase'], sep=r'\s+')

        ax = data[data['clase'] == 0].plot.scatter(figsize=(
            7.5, 7.5), x='X', y='Y', label='Clase 0', c='blue')
        data[data['clase'] == 1].plot.scatter(
            x='X', y='Y',  label='Clase 1', ax=ax, c='orange')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)

        plt.axhline(0, color='black', alpha=0.35)
        plt.axvline(0, color='black', alpha=0.35)
        print(len(data[data['clase'] == 0]))
        print(len(data[data['clase'] == 1]))
        plt.savefig(f'img/{fname}.png')
        plt.close()

        with open(f'datasets/{prefix}/{fname}.out', 'r') as f:
            data = f.readlines()
        train_e = float(get_error_number(data[len(data) - 3]))
        val_e = float(get_error_number(data[len(data) - 2]))
        test_e = float(get_error_number(data[len(data) - 1]))

        print(train_e)
        print(val_e)
        print(test_e)

        # df = pd.read_csv(f'{ex}/{outFolder}/{output}/{output}.mse',
        #                 sep='\s+', header=None, names=mse_headers)

        # print(df)
        train_err.append(train_e)
        val_err.append(val_e)
        test_err.append(test_e)
    return (train_err, val_err, test_err)


def main():
    # train_parameter('momentum', momentums, 'eta', etas, 8, 7)
    
    (train_err, val_err, test_err) = nb_train_parameter('nb')
    errors = pd.DataFrame({
        'Train': train_err,
        'Validación': val_err,
        'Test': test_err,
    }, index=bins)
    ax = errors.plot(figsize=(8, 6), title='Dos elipses', style=['.--', '.--', '.--'], color=[
                     '#cc00ff', '#d40000', '#0099cc'], xticks=list(range(10, 641, 20)).insert(0, 5))
    ax.set_xlabel('Bins')
    ax.set_ylabel('Error porcentual')
    ax.legend(loc='upper left')

    plt.savefig(f'img/nb-err-hist-dos-elipses.png')
    plt.close()

if __name__ == '__main__':
    main()
