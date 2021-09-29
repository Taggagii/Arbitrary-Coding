'''
Joke code that's really not that efficent.
Takes in a number and returns the next nubmer is forms of only 6 (+ - / or *) 9
Ex: 16 in this form could be (6+9)*6/9+6. The reason the code is written this way is so the output isn't always the same and so that by 
decreasing the number of steps will make the output longer.
'''


import random
def sixtyNineNumber(num, attempts = 10):
    options = []
    for i in range(attempts):
        current = 1
        operations = "6"
        output = 6
        level = 1
        while output != num:
            number = 9 if current else 6
            current ^= 1
            operand = random.randint(0, 1)
            if output < num:
                if operand: # add
                    output += number
                    operations += "+" + str(number)
                    level = 0
                if not operand: # mult
                    output *= number
                    if level == 0:
                        operations = "(" + operations + ")"
                    operations += "*" + str(number)
                    level = 1
            else:
                if not operand and not output % number: # divide
                    output /= number
                    if level == 0:
                        operations = "(" + operations + ")"
                    operations +=  "/" + str(number)
                    level = 1
                else:
                    output -= number
                    operations += "-" + str(number)
                    level = 0
        options.append(operations)
    try:
        outputValue = min(options, key = len)
        if eval(outputValue) == num:
            return outputValue
        else:
            return options
    except:
        return ("Error", outputValue)



def counting(previousString, attempts = 10):
    num = eval(previousString) + 1
    output = sixtyNineNumber(num, attempts)
    return (output, eval(output))

if __name__ == "__main__":
    print(counting("15", 500))
