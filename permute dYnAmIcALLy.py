'''
This code does the same as the recursive "permute.py", but, not recursively.
This is a joke code, it's just a proof of concept that you don't *need* recursion to get a job done.
'''


size = int(input("size: "))
filename = input("filename: ")

output = f"file = open('{filename}.txt', 'w')\nfor i in range(ord('a'), ord('z') + 1):"
iValues = ["chr(i)"]
for i in range(size - 1):
    iString = ''.join(['i' for x in range(i + 2)])
    iValues.append(f"chr({iString})")
    output += "\n"
    for _ in range(i + 1):
        output += '\t' # i know  i could have used '\t' * size I was just going quickly
    output += f"for {iString} in range(ord('a'), ord('z') + 1):"

output += '\n'
for _ in range(size):
    output += '\t' # i know  i could have used '\t' * size I was just going quickly
output += f"file.write({' + '.join(iValues)} + ' ')"

import time

s = time.time()
exec(output)
print(time.time() - s)


