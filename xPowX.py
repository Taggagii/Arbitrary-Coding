def xPowX(number):
    '''
    finds the value (x) that when x**x is found it will (sorta) equal the input number
    it's not a good piece of code
    oh, and the list of answer's could be much better but I'm not going to fix that just for this
    '''
    answers = [0, 1, 4, 27, 256, 3125, 46656, 823543, 16777216, 387420489, 10000000000, 285311670611, 8916100448256, 302875106592253, 11112006825558016, 437893890380859375, 18446744073709551616, 827240261886336764177, 39346408075296537575424, 1978419655660313589123979]
    if number in answers: return answers.index(number)
    number = round(float(number), 10)
    i = 0.0
    increaser = 0.01
    amount = 2
    index = str(number).index('.')
    failsafe = 0
    while True:
        try:
            i = round(i, amount) + increaser
            if i**i <= number:
                if str(i**i)[0:index] == str(number - 1)[0:index]:
                    break
            else:
                i -= increaser
                amount += 1
                increaser /= 10
        except:
            pass
    indexer = 0
    while True:
        amount += 1
        increaser /= 10
        indexer += 1
        if amount >= 17 - index:
            break
        while True:
            try:
                i = round(i, amount) + increaser
                if i**i <= number and str(i**i)[0:index] == str(number - 1)[0:index]:
                    if str(i**i)[index + indexer] == '9':
                        break
                else:
                    i -= increaser
                    amount += 1
                    increaser /= 10
                        
            except:
                pass
    return i

