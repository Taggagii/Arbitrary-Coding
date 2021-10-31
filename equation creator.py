'''
given a list of points, will create a polynomial that passes through them all. Works best with integers. Not built to be efficent in the slightest. 
This was mostly a proof of concept for a different project.
'''

import math
from sympy import *
x = Symbol('x')



def points_to_function(list_of_points):
    prev_function = 0*x + list_of_points[0][1]
    if len(list_of_points) < 2:
        return prev_function
    g = (x - list_of_points[0][0])
    lam = list_of_points[1][1] - prev_function.subs(x, list_of_points[1][0]) / g.subs(x, list_of_points[1][0])
    return simplify(ptfacc(list_of_points[1:], prev_function, g, lam))
    

def ptfacc(list_of_points, prev_function, g, lam):
    if len(list_of_points) < 2:
        return prev_function + ((lam) * g)
    function_new = prev_function + ((lam) * g)
    g_new = g * (x - list_of_points[0][0])
    lam_new = (((list_of_points[1][1] - function_new.subs(x, list_of_points[1][0]))) / g_new.subs(x , list_of_points[1][0]))
    return ptfacc(list_of_points[1:], function_new, g_new, lam_new)


def check(function, points):
    for point in points:
        if function.subs(x, point[0]) != point[1]:
            return true
    return false

import random
import time
points = [(0, 0), (1, 10), (2, 8), (3, 6), (4, 4), (5, 2), (6, 0), (7, 10)]
print(points)
#ys = [0, 10, 8, 6, 4, 2, 0, 10]
#points = [(i, ys[i]) for i in range(len(ys))]
print('start')
s = time.time()
function = points_to_function(points)
print(time.time() - s)
if check(function, points):
    print("eep")

with open("function.txt", "w") as f:
    f.write(latex(function))

with open("OTHER.txt", "w") as f:
    f.write(str(points))





