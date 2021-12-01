import math, pickle, random

def initalize_primes(size=10000000):
    values = {i: True for i in range(size)}
    for p in range(2, 1 + int(math.sqrt(size))):
        if values[p]: #this way you don't redo ones
            for i in range(p* 2, size + 1, p):
                values[i] = False
        p += 1
    values[0] = False
    values[1] = False

    with open("primes.pkl" , "wb") as f:
        pickle.dump(values, f)

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
    
def gcd(a, b):
    return eea(a, b)[2]

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

def prime_factorization(a, combine = False):
    primes = pickle.load(open("primes.pkl", "rb"))
    factorization = []
    for i in range(1, len(primes)):
        if not primes[i]: continue
        count = 0
        while not a % i:
            count += 1
            a //= i
        if count:
            if combine:
                factorization.append(i**count)
            else:
                factorization.append((i, count))
    return factorization
        

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
    

def setup(p = None, q = None):
    if p == None or q == None:
        primes = pickle.load(open("primes.pkl", "rb"))
        v = 0
        while not primes[v]:
            v = random.randint(1000000, 9999999)
        p = v

        v = 0
        while v == p or not primes[v]:
            v = random.randint(1000000, 9999999)
        q = v
        
    n = p * q
    satisfier = (p-1)*(q-1)
    
    e = satisfier
    while gcd(e, satisfier) != 1:
        e = random.randint(2, satisfier - 1)

    d = find_mult_inverse(e, satisfier)
    
    return e, d, n, p, q

def reduce_mod_power(a, power, mod):
    # put power in terms of power's of 2
    sum_p2_form = []
    while power > 0:
        value = (math.log(power) // math.log(2))
        sum_p2_form.append(value)
        power -= 2**value
        
    pows_of_two_mod = [a]
    for _ in range(int(sum_p2_form[0])):
        pows_of_two_mod.append(pows_of_two_mod[-1]**2 % mod)
        
    n = 1
    for i in sum_p2_form:
        n *= pows_of_two_mod[int(i)]
    return n % mod

        
        

def RSA_encrypt(e, n, M):
    return reduce_mod_power(M, e, n)

def RSA_decrypt(d, n, C):
    return reduce_mod_power(C, d, n)



try:
    open("primes.pkl", "rb")
except:
    print("Generating Primes...")
    initalize_primes()
    print("Primes Generated!")


e, d, n, p, q = setup(2, 11)

print(RSA_decrypt(d, n, RSA_encrypt(e, n, 5)))

