#slower than "number.as_integer_ratio()"
#REALLY SLOW

def findfraction(n):
    '''
    returns a decimal as a fraction to lowest terms
    '''
    neg = ''
    if n < 0:
        n = -n
        neg = '-'
    increase = 1
    if n > 0: increase = 10000
    boundlower, boundupper = 1, 0
    while True:
        for one in range(boundupper):
            for two in range(boundlower, boundupper):
                if one/two == n:
                    return int(neg+str(one)), two
        boundupper += increase

