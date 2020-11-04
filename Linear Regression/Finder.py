import matplotlib.pyplot as plot
import numpy, random
data = open('information.txt').read().splitlines()

x = data[0].split()
y = data[1].split()
x = [int(thing) for thing in x]
y = [int(thing) for thing in y]

averagex = sum(x)/len(x)
averagey = sum(y)/len(y)

calculate = [[] , [], [], []]
for place in range(4):
    for i in range(len(x)):
        if place == 0:
            calculate[0].append(x[i] - averagex)
        if place == 1:
            calculate[1].append(y[i] - averagey)
        if place == 2:
            calculate[2].append((x[i] - averagex)*(y[i] - averagey))
        if place == 3:
            calculate[3].append((x[i] - averagex)**2)

m = sum(calculate[2])/sum(calculate[3])
b = averagey - m*averagex
def place(x, m, b):
    return m*x + b

x.sort()
plot.scatter(x, y, color = 'red')
plot.plot((x[0] - 1, x[-1] + 1), (place(x[0] - 1, m, b), place(x[-1] + 1, m, b)))
plot.show()
