'''
does RSA stuff, it's currently a bit wonky with the math (the numbers aren't always kept small enough to be used by python)
so i may fix that, but it works for relatively large primes. 

'''

import math, pickle, random, time

def initalize_primes(size=100000000):
    values = {i: True for i in range(size)}
    for p in range(2, 1 + int(math.sqrt(size))):
        if values[p]: #this way you don't redo ones
            for i in range(p* 2, size + 1, p):
                values[i] = False
        p += 1
    values[0] = False
    values[1] = False

    primes = [i for i in values if values[i]]

    with open("all_primes_list.pkl", "wb") as f:
        pickle.dump(primes, f)
    with open("primes_dict.pkl" , "wb") as f:
        pickle.dump(values, f)
    primes = [i for i in primes if i > 1000000]
    with open("primes_list.pkl" , "wb") as f:
        pickle.dump(primes, f)
        

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
    


def eea(a, b):
    a, b = max(a, b), min(a, b)
    table = [[1, 0, a, 0], [0, 1, b, 0]]
    return eeaacc(table)

def eeaacc(table):
    if not table[1][2]:
        return table[0]
    q = table[0][2] // table[1][2]
    return eeaacc([
            [i for i in table[1]],
            [table[0][i] - q * table[1][i] for i in range(3)] + [q]])

def factorization(a, combine = False):
    prime_factors = prime_factorization(a, compress = False)
    powers = {i: 0 for i in range(len(prime_factors))}
    powers[0] = 1
##    factors = [1] # remove zero because this is used for checking coprimeness
    factors = []
    while True:
        for i in range(len(powers)):
            n = 1
            for ii in range(len(prime_factors)):
                n *= prime_factors[ii]**powers[ii]
            factors.append(n)
            if powers[i]:
                for ii in range(i, len(powers)):
                    if powers[ii]:
                        if ii == len(powers) - 1:
                            return factors
                        powers[ii] = 0
                    else:
                        powers[ii] = 1
                        break
                break
            else:
                powers[i] = 1
                break
            



def prime_factorization(a, combine = False, compress = True):
    factorization = []
    if a % 2 == 0:
        factorization.append(2)
        a //= 2
    if a % 3 == 0:
        factorization.append(2)
        a //= 3
    for i in range(5, int(math.sqrt(a))+1, 6):
        if a % i == 0:
            factorization.append(i)
            a //= i
        if a % (i + 2) == 0:
            factorization.append(i+2)
            a //= (i + 2)
    new_factors = []
    if not compress:
        return factorization
    for i in factorization:
        new_factors.append((i, factorization.count(i)))
    if combine:
        return [i[0]**i[1] for i in new_factors]
    return new_factors


##    primes = pickle.load(open("primes_list.pkl", "rb"))
##    factorization = []
##    for i in primes:
##        count = 0
##        while not a % i:
##            count += 1
##            a //= i
##        if count:
##            if combine:
##                factorization.append(i**count)
##            else:
##                factorization.append((i, count))
##    return factorization
        

def find_mult_inverse(a, mod):
    if prime(mod):
        return a**(mod-2) % mod
    
    factorization = prime_factorization(mod, combine = True)

    
    for i in range(len(factorization)):
        if prime(factorization[i]):
            factorization[i] = ((find_mult_inverse(a, factorization[i])), factorization[i])
        else:
            factorization[i] = ((brute_inverser(a, factorization[i])), factorization[i])

    #combine them
    while len(factorization) > 1:
        a, m_1 = factorization[0]
        b, m_2 = factorization[1]
        factorization[0] = (m_1 * (b - a) * find_mult_inverse(m_1, m_2) + a, m_1 * m_2)
        factorization.pop(1)
        
    return factorization[0][0] % mod

        

        
def brute_inverser(number, mod):
    n = 0
    value = (n * number) % mod
    while (value != 1):
        n += 1
        value = (n * number) % mod
    return n
    
def specialized_gcd(a, factorization_of_b):
    factorization_of_a = factorization(a)
    for i in factorization_of_b:
        if i in factorization_of_a:
            return False
    return True
    

def setup(p = None, q = None):
    if p == None or q == None:
        primes = pickle.load(open("primes_list.pkl", "rb"))
        
        p = random.choice(primes)
        q = p
        while q == p:
            q = random.choice(primes)

    n = p * q
    satisfier = (p-1)*(q-1)
    s_factorization = factorization(satisfier)
        
    e = 0
    while not specialized_gcd(e, s_factorization):
        e = random.randint(2, satisfier - 1)

    d = find_mult_inverse(e, satisfier)
    
    return e, d, n, p, q

def reduce_mod_power(b, p, mod):
    b = b % mod

    remainder = (b ** (p % 2)) % mod
    p -= p % 2

    while p != 1:
        remainder = (remainder * (b ** (p % 2))) % mod
        b = (b**2) % mod
        p //= 2

    return b*remainder % mod

##def reduce_mod_power(a, power, mod):
##    # put power in terms of power's of 2
##    sum_p2_form = []
##    while power > 0:
##        value = (math.log(power) // math.log(2))
##        sum_p2_form.append(value)
##        power -= 2**value
##        
##    pows_of_two_mod = [a]
##    for _ in range(int(sum_p2_form[0])):
##        pows_of_two_mod.append(pows_of_two_mod[-1]**2 % mod)
##        
##    n = 1
##    for i in sum_p2_form:
##        n *= pows_of_two_mod[int(i)]
##    return n % mod



try:
    open("primes_list.pkl", "rb")
    open("primes_dict.pkl", "rb")
except:
    print("Generating Primes...")
    initalize_primes()
    print("Primes Generated!")
        
e, d, n, p, q = setup()

print("Private Key:", (e, n))
print("Public Key:", (d, n))

def RSA_encrypt(M):
    global e
    global n
    return reduce_mod_power(M, e, n)

def RSA_decrypt(C):
    global d
    global n
    return reduce_mod_power(C, d, n)

def en_string(string):
    string = list(string)
    for i in range(len(string)):
        string[i] = RSA_encrypt(ord(string[i]))
    return string

def de_list(values):
    string = ""
    for i in values:
        string += chr(RSA_decrypt(i))
    return string
    





#You can only encrypt numbers that are below n, (shouldn't be a problem)

encrypted = en_string("A String that has been encrypted")

decrypted = de_list(encrypted)

print(decrypted)


