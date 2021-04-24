import subprocess, argparse
import os
from shutil import copyfile
# Utility functions
root_dir = lambda args: f'{args.mode}_{args.dvalue}d_{str(args.testsize)}'
tsize_dir = lambda args, size: f'{args.mode}_{str(size)}'

def treeAndTest(dir: str, filestem: str):
    os.chdir(dir)
    
    cmd = f'../../../R8/Src/c4.5 -f {filestem} && ../../../R8/Src/c4.5 -f {filestem} -u'
    
    res = subprocess.run(cmd,shell=True, capture_output=True)
    if(res.returncode != 0):
        print(f'Error processing: {dir}\nAborting...')
        print(res.stdout.decode('ascii'))
        return 1

    os.chdir('../../')


def names(d: int):
    cmd = ['../p0/build/names', 'C=0,1']

    for i in range(d):
        cmd += [f'-c {chr(65+i)}']

    res = subprocess.run(cmd,shell=False, capture_output=True)
    
    out = res.stdout.decode('ascii')

    if(res.returncode == 0):
        return out
    else:
        print(out)


def generate(m: str, s: int, d: int, c: float):    
    cmd = ['../p0/build/ds', '-n', str(s), '-d', str(d), '-m', m]

    if(c is not None):
        cmd += [f'-c {str(c)}']

    res = subprocess.run(cmd,shell=False, capture_output=True)
    
    out = res.stdout.decode('ascii')

    if(res.returncode == 0):
        return out
    else:
        print(out)

def main():

    """Parser definition"""
    parser = argparse.ArgumentParser('Trainer & Tester')
    parser.add_argument('mode', type=str, help='Generator mode: s:spiral|d:diagonal|p:parallel')
    parser.add_argument('testsize', type=int, help='Size of test examples')
    parser.add_argument('-i','--input', action='append', help='Add a set of input size of training examples', required=True)
    parser.add_argument('-d','--dvalue', type=int, help='Add training generated dataset of input size', default=2)
    parser.add_argument('-c','--cvalue', type=float, help='Add training generated dataset of input size')
    
    parser.add_argument('--plot', action='store_true')
    args = parser.parse_args()

    if(os.getcwd().split('/')[-1] != 'p1'):
        print('Error: this automatization tool MUST be ran in {proj_dir}/p1 folder')
        return 1
    

    """Validations"""
    if(args.mode not in ['s','d','p']):
        print('Invalid mode')
        return 1
    
    if(args.mode in ['d', 'p'] and args.cvalue is None):
        print('Diagonal (d) and Parallel (p) modes requires CVALUE argument.')
        return 1

    if(args.input is None or len(args.input) == 0):
        print('Input size of training dataset is required.')
        return 1

    dir = root_dir(args)
    if(not os.path.isdir(dir)):
        print('Root dataset directory does not exist.\nCreating it...')
        try: 
            os.mkdir(dir)
        except Exception as ex:
            print(f'Directory creation failed: {str(ex)}')
        else:
            print('Directory created succesfully!')

        # Generate test data
        test_data = generate(args.mode, args.testsize, args.dvalue, args.cvalue)
        if(test_data is None):
            print('Error generating .test file.\nAborting, please remove the generated directory.')
            return 1

        test_data_file = open(f'{dir}.test', mode='w')
        test_data_file.write(test_data)
        test_data_file.close()
        
    
    print('Dataset root directory exists.')
    for ts in args.input:
        ts_dir = tsize_dir(args, ts)
        
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
        names_ = names(args.dvalue)
        if(names_ is None):
            print('Error generating .names file.\nAborting, please remove the generated directory.')
            return 1

        names_file = open(f'{dir}/{ts_dir}/{dir}.names', mode= 'w')
        for n in map(lambda x: x.strip()+'\n',names_.splitlines()):
            names_file.write(n)
        
        names_file.close()


        train_data = generate(args.mode, ts, args.dvalue, args.cvalue)
        
        if(train_data is None):
            print(f'Error generating training data for {ts_dir}')
            return 1
        
        train_data_file = open(f'{dir}/{ts_dir}/{dir}.data', mode='w')
        train_data_file.write(train_data)
        train_data_file.close()

        if(treeAndTest(f'{dir}/{ts_dir}', dir) is not None):
            return 1




if __name__ == '__main__':
    main()

    # ll = re.search("<<$",l).string
    # re.findall('\(([^)]+)',ll)