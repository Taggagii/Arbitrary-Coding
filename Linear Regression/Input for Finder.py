#oh i wish i had a graph for all this convinentently good data


data = open('information.txt', 'w')
x = []
y = []
good = False
while True:
    if good is False:
        print('enter an x value or "close"')
        entry = input().lower()
        if entry.isdigit() is False:
            if entry == 'close':
                break
            else:
                print('incorrectly formatted input\n')
        if entry.isdigit():
            x.append(entry)
            good = True
    if good:
        print('enter a y value')
        entry = input()
        if entry.isdigit():
            y.append(entry)
            good = False
        else:
            print('incorrectly formatted input\n')
            
for thing in x:
    data.write(thing + ' ')
data.write('\n')
for thing in y:
    data.write(thing + ' ')
data.close()
import Finder
    
