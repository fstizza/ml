import subprocess
import argparse
import os
import re
from shutil import copyfile
import numpy as np
import json
from time import sleep
# Utility functions


def get_value(s: str):
    if('%' not in s):
        if('(' in s):
            return ''.join(filter(lambda x: x != '(', s))

    if('(' not in s):
        return ''.join(filter(lambda x: x != ')' and x != '%', s))

    print('HI!! : '+s)
    # ap_test_error = float(re.findall('\(([^)]+)', lns[1])[1][:-1])
    return re.findall('\(([^)]+)', s)[0][:-1]


# We create a dir for each dataset type and test examples.
def root_dir(mode: str, dvalue: int, cvalue: float, size: int):
    if(cvalue is None):
        return f'{mode}_d{str(dvalue)}_{str(size)}'

    return f'{mode}_d{str(dvalue)}_c{str(cvalue)}_{str(size)}'


def treeAndTest(dir: str, filestem: str):
    os.chdir(dir)

    res = subprocess.run(f'c4.5 -f {filestem}',
                         shell=True, capture_output=True)
    if(res.returncode != 0):
        print(f'Error processing: {dir}\nAborting...')
        return 1

    res = subprocess.run(f'c4.5 -f {filestem} -u',
                         shell=True, capture_output=True)
    if(res.returncode != 0):
        print(f'Error processing: {dir}\nAborting...')
        return 1

    lns = list(filter(lambda x: "<<" in x,
               res.stdout.decode('UTF-8').splitlines()))

    if(len(lns) != 2):
        print('Error!')
        os.chdir('../../')
        return

    train_ln = lns[0].strip()[:-2].split()
    test_ln = lns[1].strip()[:-2].split()

    tr_bp_size = int(train_ln[0].strip())
    tr_bp_error = float(re.findall('\(([^)]+)', lns[0])[0][:-1])
    tr_ap_size = int(lns[0][lns[0].index(')')+1:]
                     [:lns[0][lns[0].index(')'):].index('(')-1].split()[0])
    tr_ap_error = float(re.findall('\(([^)]+)', lns[0])[1][:-1])
    tt_bp_size = int(test_ln[0].strip())
    tt_bp_error = float(re.findall('\(([^)]+)', lns[1])[0][:-1])
    tt_ap_size = int(lns[1][lns[1].index(')')+1:]
                     [:lns[1][lns[1].index(')'):].index('(')-1].split()[0])
    tt_ap_error = float(re.findall('\(([^)]+)', lns[1])[1][:-1])

    os.chdir('../../')
    return {
        'tr_bp_size': tr_bp_size,
        'tr_bp_error': tr_bp_error,
        'tr_ap_size': tr_ap_size,
        'tr_ap_error': tr_ap_error,
        'tt_bp_size': tt_bp_size,
        'tt_bp_error': tt_bp_error,
        'tt_ap_size': tt_ap_size,
        'tt_ap_error': tt_ap_error
    }


def names(d: int):
    classes = ','.join(map(lambda x: str(x), range(d)))
    cmd = ['../p0/build/names', f'C={classes}']

    for i in range(d):
        cmd += [f'-c {chr(65+(i%26))* (int(i/26)+1)}']

    res = subprocess.run(cmd, shell=False, capture_output=True)

    out = res.stdout.decode('ascii')

    if(res.returncode == 0):
        return out
    else:
        print(out)


def generate(m: str, s: int, d: int, c: float):
    cmd = ['../p0/build/ds', '-n', str(s), '-d', str(d), '-m', m[0]]

    if(c is not None):
        cmd += [f'-c {str(c)}']

    res = subprocess.run(cmd, shell=False, capture_output=True)

    out = res.stdout.decode('ascii')

    if(res.returncode == 0):
        return out
    else:
        print(out)


def main():
    """Parser definition"""
    parser = argparse.ArgumentParser('Trainer & Tester')
    parser.add_argument('mode', type=str, choices=[
                        'spiral', 'diagonal', 'parallel'], help='Generator mode: s:spiral|d:diagonal|p:parallel')
    parser.add_argument('testsize', type=int, help='Size of test examples')
    parser.add_argument('-i', '--input', action='append',
                        help='Add a set of input size of training examples', required=True)
    parser.add_argument('-d', '--dvalue', action='append',
                        help='Add training generated dataset of input size', required=True)
    parser.add_argument('-c', '--cvalue', action='append',
                        help='Add training generated dataset of input size', required=True)
    parser.add_argument('-a', '--avg', type=int, help='Set average', default=1)

    parser.add_argument('--plot', action='store_true')
    args = parser.parse_args()

    if(os.getcwd().split('/')[-1] != 'p1'):
        print(
            'Error: this automatization tool MUST be ran in {proj_dir}/p1 folder')
        return 1

    """Validations"""
    if(args.mode in ['d', 'p'] and args.cvalue is None):
        print('Diagonal (d) and Parallel (p) modes requires CVALUE argument.')
        return 1

    stats = open(f'stats_{args.mode}', mode='w')

    stats_data = []
    for dv in args.dvalue:
        for cv in args.cvalue:
            dir = root_dir(args.mode, dv, cv, args.testsize)
            dv = int(dv)
            cv = float(cv)

            if(not os.path.isdir(dir)):
                print('Root dataset directory does not exist.\nCreating it...')
                try:
                    os.mkdir(dir)
                except Exception as ex:
                    print(f'Directory creation failed: {str(ex)}')
                else:
                    print('Directory created succesfully!')

                # Generate test data
                test_data = generate(args.mode, args.testsize, dv, cv)
                if(test_data is None):
                    print(
                        'Error generating .test file.\nAborting, please remove the generated directory.')
                    return 1

                test_data_file = open(f'{dir}.test', mode='w')
                test_data_file.write(test_data)
                test_data_file.close()

            print('Dataset root directory exists.')

            for ts in args.input:
                st = {
                    'd': dv,
                    'c': cv,
                    's': ts,
                    'tr_bp_size': 0,
                    'tr_bp_error': 0,
                    'tr_ap_size': 0,
                    'tr_ap_error': 0,
                    'tt_bp_size': 0,
                    'tt_bp_error': 0,
                    'tt_ap_size': 0,
                    'tt_ap_error': 0,
                }

                # error = (0, 0, 0, 0)
                for i in range(args.avg):
                    ts_dir = f'{str(ts)}_{str(i)}'

                    if(os.path.isdir(f'{dir}/{ts_dir}')):
                        print(f'Directory for size {str(ts)} already exists.')
                        continue

                    try:
                        os.mkdir(f'{dir}/{ts_dir}')
                    except Exception as ex:
                        print(f'Directory creation failed: {str(ex)}')
                        return 1
                    else:
                        print(f'Directory {dir}/{ts_dir} created succesfully!')

                        copyfile(f'{dir}.test', f'./{dir}/{ts_dir}/{dir}.test')

                        # Generate .names
                        names_ = names(dv)
                        if(names_ is None):
                            print(
                                'Error generating .names file.\nAborting, please remove the generated directory.')
                            return 1

                        names_file = open(
                            f'{dir}/{ts_dir}/{dir}.names', mode='w')
                        for n in map(lambda x: x.strip()+'\n', names_.splitlines()):
                            names_file.write(n)

                        names_file.close()

                        sleep(1)
                        train_data = generate(args.mode, ts, dv, cv)

                        if(train_data is None):
                            print(
                                f'Error generating training data for {ts_dir}')
                            return 1

                        train_data_file = open(
                            f'{dir}/{ts_dir}/{dir}.data', mode='w')
                        train_data_file.write(train_data)
                        train_data_file.close()

                        st_ = treeAndTest(f'{dir}/{ts_dir}', dir)
                        st = merge_stats(st, st_)

                avg = avg_stats(st, args.avg)

                stats_data.append(avg)
                
    stats.write(json.dumps(stats_data))


def avg_stats(this: dict, avg: int):
    this['tr_bp_size'] = this['tr_bp_size'] / avg
    this['tr_bp_error'] = this['tr_bp_error'] / avg
    this['tr_ap_size'] = this['tr_ap_size'] / avg
    this['tr_ap_error'] = this['tr_ap_error'] / avg
    this['tt_bp_size'] = this['tt_bp_size'] / avg
    this['tt_bp_error'] = this['tt_bp_error'] / avg
    this['tt_ap_size'] = this['tt_ap_size'] / avg
    this['tt_ap_error'] = this['tt_ap_error'] / avg
    return this


def merge_stats(this: dict, other: dict):
    this['tr_bp_size'] = this['tr_bp_size'] + other['tr_bp_size']
    this['tr_bp_error'] = this['tr_bp_error'] + other['tr_bp_error']
    this['tr_ap_size'] = this['tr_ap_size'] + other['tr_ap_size']
    this['tr_ap_error'] = this['tr_ap_error'] + other['tr_ap_error']
    this['tt_bp_size'] = this['tt_bp_size'] + other['tt_bp_size']
    this['tt_bp_error'] = this['tt_bp_error'] + other['tt_bp_error']
    this['tt_ap_size'] = this['tt_ap_size'] + other['tt_ap_size']
    this['tt_ap_error'] = this['tt_ap_error'] + other['tt_ap_error']
    return this


# Limpiar los .test del root.
if __name__ == '__main__':
    main()
