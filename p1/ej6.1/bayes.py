from os import listdir

from enum import Enum

def bayes(filestem:str):
    
    dirs = sorted(filter(lambda x: filestem in x,listdir()))

    errors_per_fs = []
    for dir in dirs:
        errors = 0
        test_file = open(dir, mode='r')

        test_ex = test_file.readlines()

        for test in test_ex:
            inputs = test.split(',')

            if(filestem == 'diagonal'):
                    # Nos fijamos el signo la suma de todas las componentes
                belongs_to = int(inputs[-1])

                classified_as = None

                if(sum(map(lambda x: float(x),inputs[:-1])) > 0):
                    classified_as = 0
                else: 
                    classified_as = 1
                    
                if(classified_as != belongs_to):
                    errors += 1

            if(filestem == 'parallel'):
                belongs_to = int(inputs[-1])

                classified_as = None
                
                if(float(inputs[0]) > 0):
                    classified_as = 0
                else: 
                    classified_as = 1
                    
                if(classified_as != belongs_to):
                    errors += 1

        errors_per_fs.append(errors)
    print(errors_per_fs)
        
if __name__ == '__main__':
    print('Diagonal minimal error:')
    bayes('diagonal')
    print('Parallel minimal error:')
    bayes('parallel')