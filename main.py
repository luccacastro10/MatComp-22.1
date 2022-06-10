from municipio import municipio
import math
import numpy as np
import matplotlib.pyplot as plt

def leastSquares(points):

    #point[0] = x
    #point[1] = y
    n = len(points)
    print("VALOR DE N:" + str(n))
    
    xSum  = 0
    ySum  = 0
    x2Sum = 0
    xySum = 0

    for point in points:
        xSum  += point[0]
        ySum  += point[1]
        x2Sum += point[0]**2
        xySum += point[0]*point[1]

    m = ((n*xySum) - (xSum*ySum))/((n*x2Sum) - (xSum**2))
    n = (ySum - (m*xSum))/n

    return [m,n]

def logisticRegression(points):

    #descobrir a, b e c
    a = 0
    b = 0
    c = 0

    t = []
    p = []
    p1 = []     #p_t
    p2 = []     #p_t+1
    z = []

    for point in points:
        t.append(point[0])
        p.append(point[1])
    
    p1 = p[:(len(p)-1)]
    p2 = p[1:]

    print("\n\nt:"     + str(t))
    print("p: "    + str(p) + "\n")
    print("pi: "   + str(p1))
    print("pi+1: " + str(p2) + "\n")

    firstRegression = []
    for i in range(len(p1)):
        point = []
        point.append(p1[i])
        point.append(p2[i])
        firstRegression.append(point)

    print("first: " + str(firstRegression) + "\n")
    firstResult = leastSquares(firstRegression)

    print("m: " + str(firstResult[0]))
    print("n: " + str(firstResult[1]) + "\n")

    a = (firstResult[1]/(1-firstResult[0]))

    print("a: " + str(a))

    for pt in p1:
        z.append(math.log(pt/a) - math.log(1-pt/a))

    print("z: " + str(z) +"\n")

    secondRegression = []
    for i in range(len(p1)):
        point = []
        point.append(t[i])
        point.append(z[i])
        secondRegression.append(point)

    print("second: " + str(secondRegression) + "\n")

    secondResult = leastSquares(secondRegression)

    c = secondResult[0]
    b = math.exp(secondResult[1])

    return [a,b,c]

def plotLogistic(result):
    a = result[0]
    b = result[1]
    c = -result[2]

    x = np.linspace(-np.pi,np.pi,10000)
    y = a/(b*np.exp(c*x)+1)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.plot(x,y, 'b')
    plt.show()
















rj = municipio("rj", "data/municipio.txt")
rj.loadPoints()
# rj.generateGraph()


# print(leastSquares(rj.points))
result = logisticRegression(rj.points)
print(result)
rj.generateGraph()
plotLogistic(result)




