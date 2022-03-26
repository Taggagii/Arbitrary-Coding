'''
Quick code to help me in grade 12 Calculus so I didn't have to write tables by hand. Because I didn't like doing that I guess.
'''
from math import inf, sin, cos, pi
equation = input("enter the equation: ").replace('x', '(x)')

approaching = eval(input("what value is being approached?: "))

if approaching is not inf:
    approaching = int(approaching)

#direction = input("From which direction? (left, right, or both): ")

    check_values = [0.5] + [1 / 10 ** i for i in range(1, 10)]
    left, right = [], []

    for value in check_values:
        left.append(approaching - value)
        right.append(approaching + value)
    left.append(approaching), right.append(approaching)
else:
    left = [-approaching]
    right = [approaching]

#evaluate each x value

for list_of_values in [(right, "RIGHT"), (left, "LEFT")]:
    print(list_of_values[1])
    for i in list_of_values[0]:
        try:
            value = eval(equation.replace("x", str(i)))
            if isinstance(value, complex):
                print(i, "|", "complex")
            else:
                print(i, "|", value)
        except Exception as e:
            print(i, "|", "DNE")
    print()
    
    




