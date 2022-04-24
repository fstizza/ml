import matplotlib.pyplot as plt, argparse as ap
import json
from os import path, listdir

def ej5():
    stats_file = open('stats_diagonal', mode='r')
    stats = json.load(stats_file)

    # Ejercicio 5
    sizes = list(map(lambda x: x['s'], stats))

    # 
    tr_ap_errors = []
    tt_ap_errors = []
    tt_ap_sizes = []
    for s in stats:
        tr_ap_errors.append(s['tr_ap_error'])
        tt_ap_errors.append(s['tt_ap_error'])
        tt_ap_sizes.append(s['tt_ap_size'])

    fig, axs = plt.subplots(3,1 , squeeze=False)


    axs[0][0].plot(sizes, tr_ap_errors)
    axs[0][0].set_title('Training error (%)')
    axs[1][0].plot(sizes, tt_ap_errors)
    axs[1][0].set_title('Test error (%)')
    axs[2][0].plot(sizes, tt_ap_sizes)
    axs[2][0].set_title('Tree size after pruning (test)')
    
    stats_file = open('stats_parallel', mode='r')
    stats = json.load(stats_file)

    # Ejercicio 5
    sizes = list(map(lambda x: x['s'], stats))

    # 
    tr_ap_errors = []
    tt_ap_errors = []
    tt_ap_sizes = []
    for s in stats:
        tr_ap_errors.append(s['tr_ap_error'])
        tt_ap_errors.append(s['tt_ap_error'])
        tt_ap_sizes.append(s['tt_ap_size'])

    axs[0][0].plot(sizes, tr_ap_errors)
    axs[0][0].set_xscale('log')
    axs[0][0].legend(["diagonal", "parallel"], loc ="lower right")

    axs[1][0].plot(sizes, tt_ap_errors)
    axs[1][0].set_xscale('log')
    axs[1][0].legend(["diagonal", "parallel"], loc ="lower right")
    
    axs[2][0].plot(sizes, tt_ap_sizes)
    axs[2][0].set_xscale('log')
    axs[2][0].legend(["diagonal", "parallel"], loc ="lower right")

    plt.savefig('ej5.jpg')
    
    plt.show()

def ej6():
    stats_file = open('stats_diagonal', mode='r')
    stats = json.load(stats_file)

    # Ejercicio 5
    cvalues = list(map(lambda x: x['c'], stats))

    # 
    tt_bp_errors = []
    tt_ap_errors = []
    for s in stats:
        tt_bp_errors.append(s['tt_bp_error'])
        tt_ap_errors.append(s['tt_ap_error'])

    plt.plot(cvalues, tt_bp_errors)
    plt.plot(cvalues, tt_ap_errors)

    stats_file = open('stats_parallel', mode='r')
    stats = json.load(stats_file)
    cvalues = list(map(lambda x: x['c'], stats))

    tt_bp_errors = []
    tt_ap_errors = []
    for s in stats:
        tt_bp_errors.append(s['tt_bp_error'])
        tt_ap_errors.append(s['tt_ap_error'])

    plt.plot(cvalues, tt_bp_errors)
    plt.plot(cvalues, tt_ap_errors)

    diag_min_error = list(map(lambda x: x / 100, [159, 666, 1094, 1434, 1670]))
    plt.plot(cvalues, diag_min_error)

    par_min_error = list(map(lambda x: x / 100, [261, 1628, 2525, 3170, 3386]))
    plt.plot(cvalues, par_min_error)
    
    plt.legend(["diagonal_test_error_bp", "diagonal_test_error_ap", "parallel_test_error_bp", "parallel_test_error_ap", "diagonal_min_error", "parallel_min_error"], loc ="lower right")
    
    plt.savefig('ej6.jpg')
    plt.show()

def ej7():
    stats_file = open('stats_diagonal', mode='r')
    stats = json.load(stats_file)

    # Ejercicio 5
    dvalues = list(map(lambda x: x['d'], stats))

    # 
    tr_bp_errors = []
    tt_bp_errors = []
    for s in stats:
        tr_bp_errors.append(s['tr_bp_error'])
        tt_bp_errors.append(s['tt_bp_error'])

    plt.plot(dvalues, tr_bp_errors)
    plt.plot(dvalues, tt_bp_errors)

    stats_file = open('stats_parallel', mode='r')
    stats = json.load(stats_file)

    dvalues = list(map(lambda x: x['d'], stats))

    tr_bp_errors = []
    tt_bp_errors = []
    for s in stats:
        tr_bp_errors.append(s['tr_bp_error'])
        tt_bp_errors.append(s['tt_bp_error'])

    plt.plot(dvalues, tr_bp_errors)
    plt.plot(dvalues, tt_bp_errors)

    plt.legend(["diagonal_train_error_bp", "diagonal_test_error_bp", "parallel_train_error_bp", "parallel_test_error_bp"], loc ="lower right")
    
    plt.savefig('ej7.jpg')
    plt.show()

def plot_prediction(filestem: str):
    
    dims = int(next(filter(lambda x: x.startswith('d'), filestem.split('_')), None)[1:])
    if(dims != 2):
        print('Cannot plot >2 dimensions')
        return 1
    
    dirs = list(filter(lambda x: path.isdir(f'{filestem}/{x}'), listdir(filestem)))
    
    pls = []
    for p in dirs:
        pr = open(f'{filestem}/{p}/{filestem}.prediction')
        lines = pr.readlines()
        pr.close()

        vals0 = ([],[])
        vals1 = ([],[])
        
        for ln in lines:
            data = ln.split()
            if(data[-1] == '0'):
                x,y = vals0
                x.append(float(data[0]))
                y.append(float(data[1]))
            else:
                x,y = vals1
                x.append(float(data[0]))
                y.append(float(data[1]))
        
        pls.append((vals0, vals1))

    plots = list(zip(pls, dirs))

    fig, axs = plt.subplots(1, len(pls), squeeze=False)

    for pl in range(len(plots)):
        (c0, c1), name = plots[pl]
        x0, y0 = c0
        x1, y1 = c1
        axs[0][pl].set_title(name)
        axs[0][pl].scatter(x0,y0)
        axs[0][pl].scatter(x1,y1)
        
    plt.savefig(f'{filestem}/predictions.jpg')
    plt.show()

def main():
    parser = ap.ArgumentParser('Plotter')
    parser.add_argument('-p', '--prediction', type=str)
    parser.add_argument('-e', '--exercise', choices=['5','6','6.1','7'])
    args = parser.parse_args()

    if(args.prediction == None and args.exercise == None):
        print('Error')
        return 1

    if(args.prediction != None and args.exercise != None):
        print('Error')
        return 1

    if(args.prediction != None):
        plot_prediction(args.prediction)
    
    if(args.exercise != None):
        if(args.exercise == '5'):
            return ej5()
        elif(args.exercise == '6'):
            return ej6()
        elif(args.exercise == '6.1'):
            pass
        elif(args.exercise == '7'):
            return ej7()

if __name__ == '__main__':
    main()
    


