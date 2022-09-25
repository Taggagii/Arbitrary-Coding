'''
    allows for permuting of many different types of objects (strings, lists, and integers). I made this mostly for the integer part, to see if a swap function for integers made any sense
'''

import math

def lemma(number):
    return int(math.log10(number)) + 1

def getDigit(number, a):
    return number // math.floor(10**(lemma(number) - a - 1)) % 10

def insertAtI(number, a, i):
    s = 10**(lemma(number) - i)
    return (((number // s) * 10 + a) * s) + (number % s)

def replaceAtI(number, a, i):
    s = 10**(lemma(number) - i - 1)
    return (((number // (10**(lemma(number) - i))) * 10 + a) * s) + (number % s)

def swapInt(number, a, b):
    return replaceAtI(replaceAtI(number, getDigit(number, a), b), getDigit(number, b), a)

def swapList(lst, a, b):
    lst[a], lst[b] = lst[b], lst[a]
    return lst

def swap(value, a, b):
    if (isinstance(value, int)):
        return swapInt(value, a, b)
    if (isinstance(value, list)):
        return swapList(value, a, b)

def myLength(value):
    if (isinstance(value, int)):
        return lemma(value)
    if (isinstance(value, list)):
        return len(value)
    if (isinstance(value, str)):
        return len(value)

def permuteIterative(lst):
    length = myLength(lst)

    c = [0 for i in range(length)]
    outputs = [lst]

    isString = isinstance(lst, str)
    if (isString):
        lst = list(lst)

    i = 1
    while i < length:
        if c[i] < i:
            if i & 1:
                lst = swap(lst, c[i], i)
            else:
                lst = swap(lst, 0, i)
            if (isString):
                outputs.append("".join(lst))
            else:
                outputs.append(lst)
            c[i] += 1
            i = 1
        else:
            c[i] = 0
            i += 1
    return outputs


print(permuteIterative(['a', 'b', 'c']))
print(permuteIterative('abc'))
print(permuteIterative(123))


    


