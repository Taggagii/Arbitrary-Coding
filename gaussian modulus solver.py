from fractions import Fraction as fr

# can be used when given a system of congruences that have all the same
# modulus and the modulus is prime

def printm(matrix):
    for i in matrix:
        print(i)
        
def gsolve(matrix):
    width = len(matrix[0])
    height = len(matrix)
    for i in range(height):
        for ii in range(width):
            matrix[i][ii] = fr(matrix[i][ii], 1)
            
    for pivot in range(height):
        #printm(matrix)
        # pivot
        div = matrix[pivot][pivot]
        for i in range(width):
            matrix[pivot][i] = fr(matrix[pivot][i], div)

        # eliminate row
        for row in range(height):
            if row == pivot: continue
            multer = matrix[row][pivot]
            for i in range(width):
                matrix[row][i] = matrix[row][i] - matrix[pivot][i] * multer
            
    return [i[-1] for i in matrix]

def find_inverse(number, prime):
    return number ** (prime - 2) % prime

def pack_solve_to_mod(solutions, mod):
    for i in range(len(solutions)):
        denom = solutions[i].denominator
        solutions[i] = (solutions[i].numerator * find_inverse(denom, mod)) % mod
    return solutions

#example

matrix = [
    [3, 2, 22, 1],
    [7, 21, 1, 2],
    [4, 3, 1, 9]
    ]

thing = gsolve(matrix)
print(pack_solve_to_mod(thing, 23))
