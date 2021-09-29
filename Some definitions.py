''' 
compilation of commonly helpful functions I'd regarded as possibly useful in the future. From my time doing project euler
'''

import math
    
def fibs(amount):
    '''
    function for finding fibonacci numbers up to a given amount
    '''
    values = [0, 1] #making a list with the first two fibonacci numbers
    if not isinstance(amount, int) or amount < 0: #error checking for non-int or negative inputs
        return []
    if amount < 2: #returning early if amount is below 2
        return values[:amount]
    for i in range(amount - 2):
        values.append(values[-1] + values[-2]) #appends the sum of the previous two numbers to "values"
    return values

def primes_sieve(to):
    '''
    returns primes to a number using the sieve
    '''
    primes = [True for i in range(to + 1)]
    p = 2
    while (p * p <= to):
        if (primes[p] == True):
            for i in range(p * 2, to + 1, p):
                primes[i] = False
        p += 1
    primes[0] = False
    primes[1] = False
    newprimes = []
    for i in range(len(primes)):
        if primes[i]:
            newprimes.append(i)    
    return newprimes


primes = prime_sieve(100000)

def phi(n):
    '''
    euler's totient function
    '''
    value = n
    for prime in primes:
        if n % prime == 0:
            value *= (1 - (1/prime))
        else: break
        if prime > n: break
    return value


def gen_primes():
    '''
    generates primes i guess
    '''
    yield 2
    n = 3
    while True:
        yield n
        n += 2
        while not prime(n):
            n += 2

def list_of_prime_factors(to):
    '''
    returns the number of primes factors
    '''
    factors = [0] * to
    for number in range(2, to):
        if factors[number] == 0:
            for multiple in range(2*number, to, number):
                factors[multiple] += 1
    return factors
 
def prime(n):
    """
    returns true or false depending if a number is a prime or not
    """
    n = int(n)
    if n <= 3: return n > 1
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, int(math.sqrt(n))+1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def primorial(upper):
    '''
    returns the primorial under a certain upper value
    '''
    primorial, value = 2, 1
    while primorial < upper:
        value += 2
        if prime(value):
            primorial *= value
    return primorial//value

def list_of_primes(length):
    """
    returns a list of primes numbers of a specified length
    """
    primes, counter, value = [2], 1, 1
    while True:
        value += 2
        if prime(value):
            primes.append(value)
            counter += 1
        if counter == length:
            return primes

def sumdigits(number):
    '''
    sums the digits of a number
    '''
    number = int(number)
    remainder = 0
    while number:
        remainder, number = remainder + number % 10, number // 10
    return remainder

def list_of_primes_to(start, end):
    """
    returns a list of primes numbers to a number
    """
    if start % 2 == 0: start -= 1
    i = start
    if start < 2:
        primes = [2, 3]
    else:
        primes = []
    while True:
        i += 2
        if prime(i):
            primes.append(i)
            if i >= end:
                return primes

def parts(word):
    """
    returns a list of strings of the sections of a inputted number or string
    """
    word = str(word)
    parts = []
    start, end = 0, len(word)
    while True:
        parts.append(word[start:end])
        end -= 1
        if end == start:
            end = len(word)
            start += 1
        if end == start:
            return parts

def interior_primes(number):
    """
    returns a list of all the primes included in a number
    """
    sections = parts(number)
    primes = []
    for i in sections:
        if prime(int(i)):
            primes.append(i)
    return primes

def check_pandigital(number):
    '''
    checks if a value is pandigital (1-9 only once, no 0)
    '''
    number = str(number)
    if len(number) != 9: return False
    number = [int(i) for i in str(number)]
    for i in range(1, 10):
        try:
            number.remove(i)
        except:
            return False
    if sum(number) != 0: return False
    return True

def check_pandigital_from_zero(number):
    '''
    checks if a value is pandigital (0-9 only once)
    '''
    number = str(number)
    if len(number) != 10: return False
    number = [int(i) for i in str(number)]
    for i in range(10):
        try:
            number.remove(i)
        except:
            return False
    if sum(number) != 0: return False
    return True

def give_concat(base, n):
    '''
    returns the multiples of the base times n together as a string... for some reason
    '''
    base = int(base)
    values = []
    for i in range(1, n+1):
        values.append(str(base*i))
    return ''.join(values)

def findfraction(n):
    '''
    returns a lowest fractions
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

def which_pandigital(number, from_zero = False):
    '''
    checks which pandigital the value is
    '''
    number = str(number)
    if '0' in number and not from_zero: return 0
    start = 1
    if from_zero: start = 0
    for i in range(start, 10):
        if number.count(str(i)) != 1:
            if i == 0: i = 1
            return i-1
    return 9
def find_alpha_value(letter):
    '''
    returns alphabetical value of a letter
    '''
    return ord(letter.lower())-96

def find_alpha_sum(word):
    '''
    returns the sum of the alphabetical values of a word
    '''
    word = [i for i in word.lower()]
    summ = 0
    for i in word:
        summ += find_alpha_value(i)
    return summ

def triangle_number(number):
    '''
    returns either true or false if a number if a triangle number
    '''
    return (-1+math.sqrt(1+8*number))%2 == 0
        
def factorial(x):
    '''
    returns factorial of a number
    '''
    prod = 1
    for i in range(2, x+1):
        prod *= i
    return prod

def choose(n, k):
    '''
    is n choose k
    '''
    return factorial(n)/(factorial(k)*factorial(n-k))

def rotations(number):
    '''
    returns the rotations of a number
    '''
    rotations = []
    for i in range(len(str(number))):
        number = [i for i in str(number)]
        newthing = [number[-1]]
        for i in range(1, len(number)):
            newthing.append(number[i-1])
        number = ''.join(newthing)
        rotations.append(int(number))
    return rotations

def palindrome(number):
    '''
    returns if something is a palindrome
    '''
    number = str(number)
    return number == number[::-1]

def trunctate(number):
    '''
    returns the sections from a number
    '''
    final = []
    number = [i for i in str(number)]
    for i in range(1, len(number)):
        final.append(number[i:])
    for i in range(1, len(number)):
        final.append(number[0:-i])
    return [int(''.join(i)) for i in final]

def swap(index_one, index_two, list):
    '''
    swaps two index's in a list
    '''
    holder = list[index_one]
    list[index_one] = list[index_two]
    list[index_two] = holder
    return list

def permutations(string, no_of_permutations, output_all=False):
    '''
    returns all permutations of a string or number
    '''
    string = [i for i in str(string)]
    if output_all: outputs = []
    length = len(string)
    for i in range(no_of_permutations):
        one = length - 1
        two = length
        while string[one-1] >= string[one]: one -= 1
        while string[two-1] <= string[one -1]: two -= 1
        string[one-1], string[two-1] = string[two-1], string[one-1]
        one += 1
        two = length
        while one < two:
            string[one-1], string[two-1] = string[two-1], string[one-1]
            one += 1
            two -= 1
            if output_all: outputs.append(''.join(string))
    if output_all: return outputs
    return ''.join(string)

def length_decimal_repeat(denom):
    '''
    returns the length of the repeating decimal of a denominator under 1
    '''
    starter = 1
    remainder = []
    while True:
        starter %= denom
        if starter in remainder: break
        remainder.append(starter)
        starter *= 10
    return len(remainder)

def pentagonal_number(number):
    '''
    checks if a number is a pentagonal number
    '''
    return (math.sqrt(24*number + 1) + 1) % 6 == 0
def pentagonal_number_at(n):
    '''
    returns a pentagonal number at the place n
    '''
    return n*(3*n-1)//2

def hexagonal_number_at(n):
    '''
    returns a hexoagonal number at the place n
    '''
    return n*(2*n-1)

def hexagonal_number(number):
    '''
    checks if a number is hexagonal
    '''
    return ((1 + math.sqrt(1 + 8 * number)))%4==0

def twice_square(number):
    '''
    checks if a number is twice a square
    '''
    return (math.sqrt(number/2)) == float(int((math.sqrt(number/2))))
import numpy as np

def primefactors(n):
    '''
    returns the prime factors of a number
    '''
    factors = []
    i = 2
    while i * i <= n:
        if n%i == 0:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def GCF(one, two):
    '''
    returns the greatest common factor of two numbers using the euclidean algorithm
    '''
    smaller = min(one, two)
    bigger = max(one, two)
    q, r = divmod(bigger, smaller)
    previous = 1
    while True:
        if r == 0: return previous
        previous = r
        bigger = smaller
        smaller = r
        q, r = divmod(bigger, smaller)




def numberofprimefactors(number, list):
    '''
    the name
    '''
    nod = 0
    pf = False
    remain = number

    for i in range(len(list)):
        if list[i] * list[i] > number:
            return nod + 1
        pf = False
        while remain % list[i] == 0:
            pf = True
            remain /= list[i]
        if pf:
            nod += 1
        if remain == 1:
            return nod
    return nod

def sum_of_consecutive_primes(number, primes):
    '''
    if it is the sum of consecutive primes, will return a list of them
    else returns False
    '''
    summ = 0
    numbers = []
    for prime in primes:
        summ += prime
        numbers.append(prime)
        if summ == number: return len(numbers)
        if summ > number:
            for prime2 in primes:
                summ -= prime2
                numbers.remove(prime2)
                if summ == number: return len(numbers)
                if summ < number: return 0

def largest_prime_factor(n):
    '''
    returns the largest prime factor of a number
    '''
    prime_factor = 1
    i = 2
    while i <= n // i:
        if n % i == 0:
            prime_factor = i
            n //= i
        else:
            i += 1
    if prime_factor < n:
        prime_factor = n
    return prime_factor

def lychrel(number):
    '''
    returns if a number cant be reversed and added to give a plaindrome
    '''
    summ = number
    number = [i for i in str(number)]
    counter = 0
    for i in range(50):
        number = [i for i in str(summ)]
        number.reverse()
        counter += 1
        summ += int(''.join(number))
        if palindrome(summ):
            return False
    return True

def lemma(n):
    '''returns the length of a nubmer'''
    return int(1 + math.log10(n))

def first_digits_of_power(base, power, digits):
    '''
    for a given base and power, returns the number of digits specified from the beginning
    '''
    return int(10**(power * math.log10(base) - (1 + int(power * math.log10(base))) + digits))


def sqrt_to(n, amount=10):
    if 1 <= n < 100: decimal_place = 1
    else: decimal_place = int(1 + math.log10(n))//2
    a, b = 5*n, 5
    amount += 2
    while True:
        if len(str(b)) == amount:
            b = str(b)
            return str(int('0' + b[:decimal_place])) + '.' + b[decimal_place:-2]
        if a >= b:
            a -= b
            b += 10
        if a < b:
            a *= 100
            b = str(b)
            b = int(b[:len(b)-1] + '05')
    


    
