import time

#someone made a very long and verbose and, frankly, painful unit converter in my class (consisted of at least 100 if statements). They told me there "wasn't an easier way" and challanged me to make a better one
#I made something which was more expandable and much smaller. Perhaps at the cost of simplisity

#to expand: add values into amounts and units that correspond to their base value for their unit thing (distance, weight, etc.)
#keep them in the right order
amounts = [0.3048, 0.4572, 1.0, 1609.34, 9460730472580800]
units = ['foot', 'ft', 'cubit', 'cu', 'metre', 'm', 'mile', 'mi',
         'light year', 'ly']
while True:
    try:
        print('units:')
        counter = 0
        for unit in units:
            print(unit, end = '')
            counter += 1
            if counter == 2:
                print()
                counter = 0
            else:
                print(', ', end = '')
        while True:
            print('\nenter the base unit to convert')
            base_unit = input().lower()
            if base_unit in units:
                break
        while True:
            try:
                print('the amount of that unit')
                base_amount = int(input())
                break
            except:
                pass
        if units.index(base_unit) % 2 != 0:
            base_unit = units[units.index(base_unit)-1]
        amount = amounts[int(units.index(base_unit)/2)]
        while True:
            print('and what do you want it converted to?')
            to_unit = input().lower()
            if to_unit in units:
                break

        if units.index(to_unit) % 2 != 0:
            to_unit = units[units.index(to_unit)-1]
        to_amount = amounts[int(units.index(to_unit)/2)]
        new_amount = (base_amount * amount) / to_amount
        small_unit = units[units.index(to_unit)+1]
        print(f'converted: {new_amount}{small_unit}\n')
    except:
        pass

