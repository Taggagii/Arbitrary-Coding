'''
generally slower than newton's method. point was to see the inviability of this method, though it could probably be better if I was better with math.
'''


from sympy import symbols, solve, sqrt
from sympy.solvers import solve
from sympy.plotting import plot

x = symbols('x')
a = symbols('a')


# approxmiation = approxmiation.subs(a, var_a)

# plot(approxmiation, show = True)

def find_root(function, starting_point = 0):
    derivative = function.diff(x)
    second_derivative = derivative.diff(x)

    approxmiation = (1/2)*second_derivative.subs(x, a)*(x-a)**2 + derivative.subs(x, a)*(x-a) + function.subs(x, a)

    # should add something to catch if the approximation is not quadratic, if so then proceed by newtons method
    # otherwise use the quadratic formula

    # non-negative when there are solutions
    descriminant = (derivative.subs(x, a))**2 - 2*second_derivative.subs(x, a)*function.subs(x, a)

    var_a = starting_point

    M = descriminant.subs(a, var_a)

    derivative_frac = derivative.subs(x, a)/second_derivative.subs(x, a)
    # use the vertex while there are no solutions
    while M < 0:
        var_a -= derivative_frac.subs(a, var_a)
        M = descriminant.subs(a, var_a)
    
    # if you look at both roots then you could find multiple roots with the same starting computation 

    # this part needs to be cleaner to be more efficent, most of the time is lost in computing the roots over and over even though we don't need them
    # to go to one root
    n_c = (derivative.subs(x, a) - sqrt((derivative.subs(x, a))**2 - 2*second_derivative.subs(x, a)*function.subs(x, a)))/second_derivative.subs(x, a)

    # to go to the other root
    n_f = (derivative.subs(x, a) + sqrt((derivative.subs(x, a))**2 - 2*second_derivative.subs(x, a)*function.subs(x, a)))/second_derivative.subs(x, a)

    def abs_min(a, b):
        if abs(a) < abs(b):
            return a
        return b

    # go to the closest root
    for _ in range(10):
        # move to the closest root
        var_a -= abs_min(n_f.evalf(subs={a: var_a}), n_c.evalf(subs={a: var_a}))

    # return the root after an arbitary number of iterations
    return var_a
    
# for reference
def newtons_method(function, starting_point = 0):
    derivative = function.diff(x)

    M = function/derivative

    var_a = starting_point

    for i in range(10):
        var_a -= M.subs(x, var_a).evalf()
    
    return var_a.evalf()


function = x**3 + 2*x**2 + 3*x + 2

