'''
A quick code to help me in grade 12 calculus to check over my homework answers to make sure I was right.
'''
from sympy import *
import matplotlib.pyplot as plot
from numpy import arange
import os
x = Symbol('x')
while True:
    try:
        equation = input("enter the equation: ")
        derivative = diff(equation, x)
        derivative2 = diff(derivative, x)

        x_intercepts = solve(equation, x)
        crit_numbers = solve(derivative, x)
        inflection_numbers = solve(derivative2, x)\

        x_intercepts_points = [(i, 0) for i in x_intercepts]
        crit_points = [(i, eval(equation.replace('x', f"({str(i)})"))) for i in crit_numbers]
        inflection_points = [(i, eval(equation.replace('x', f"({str(i)})"))) for i in inflection_numbers]

        os.system('clear')
        print("y =", equation)
        print("y` =", derivative)
        print("y`` =", derivative2)
        print()
        
        print("x-intecepts:")
        for i in x_intercepts_points:
            if "i" not in str(i[0]).lower():
                print(i)
        print()
        
        print("critical points:")
        for i in crit_points:
            
            print(i, end = " => ")
            try:
                value = eval(str(derivative2).replace('x', '(' + str(i[0]) + ')'))
                print('max' if value < 0 else 'min' if value > 0 else 'saddle')
            except Exception as e:
                print("could not obtain")
        print()

        print("inflection points:")
        for i in inflection_points:
            print(i)
        print()
        all_points = x_intercepts + crit_numbers + inflection_numbers

        def grapher(start, stop, step = 0.1):
            x = arange(start, stop, step)
            y = eval(equation)
            plot.plot(x, y)
            plot.axhline(y = 0, color = "black")
            plot.axvline(x = 0, color = "black")
            plot.show()

        grapher(min(all_points) - 1, max(all_points) + 1)
            
        break
    except Exception as e:
        print("Something has gone wrong, please retry")
        print(e)
        pass
