import getopt, sys, math, matplotlib.pyplot as plt
from subprocess import run
from mpl_toolkits.mplot3d import Axes3D

def main():
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "m:n:d:c:", ["help", "output="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    m = 'a'
    n = 200
    d = 2
    c = 0.75

    for o, a in opts:
        if o == '-m':
            m = a
        elif o == '-n':
            n = int(a)
        elif o == '-d':
            d = int(a)
        elif o == '-c':
            c = float(a)
            
    cmd = ['./build/ds'] + (sys.argv[1:])
    res = run(cmd, capture_output=True)
    data = res.stdout.decode('ascii').splitlines(keepends= False)
    
    data = list(map(lambda i: list(map(lambda x: x.strip(), i.split(','))), data))
    c0 = list(map(lambda y: y[:d], list(filter(lambda x: x[d] == '0',data))))
    c1 = list(map(lambda y: y[:d], list(filter(lambda x: x[d] == '1',data))))


    g_axis = None
    if(m == 'a'):
        c = c * math.sqrt(d)
        g_axis = [-5*c,5*c,-5*c,5*c]
    elif(m == 'b'):
        g_axis = [-5*c,5*c,-5*c,5*c]
    elif(m == 'c'):
        g_axis = [-1,1,-1,1]


    if(d == 2):
        xs,ys = points(c0,d)
        plt.scatter(xs,ys)
        xs,ys = points(c1,d)
        plt.scatter(xs,ys)
        plt.axis(g_axis)
        plt.show()
    elif(d == 3):
        fig = plt.figure()
        ax = Axes3D(fig, auto_add_to_figure=False)
        
        xs,ys,zs = points(c0,d)
        ax.scatter(xs,ys,zs)

        xs,ys,zs = points(c1,d)
        ax.scatter(xs,ys,zs)
        
        fig.add_axes(ax)
        plt.show()

    else:
        print("Error, no se pueden graficar datos de {0} dimensiones.".format(d))
        return
        

def points(c, d):
    xs = []
    ys = []
    zs = []
    if(d == 2):
        for i in c:
            x,y = i
            xs.append(float(x))
            ys.append(float(y))
        return (xs,ys)
    if(d == 3):
        for i in c:
            x,y,z = i
            xs.append(float(x))
            ys.append(float(y))
            zs.append(float(z))
        return (xs,ys,zs)
    

if __name__ == '__main__':
    main()