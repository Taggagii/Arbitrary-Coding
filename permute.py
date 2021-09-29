'''
Recursively generates the permutations of a set length of lower case letters (eg. 2 => aa ab ba bb).
Writes the output to a file. BE AWARE THIS CODE GENERATES REALLY LARGE FILES REALLY QUICKLY, SO DON'T PUT IN A NUMBER LARGER THAN 5 OR SO UNLESS YOU HAVE THE SPACE (which you don't) TO STORE IT.
I wrote this to see if it would run faster using the GPU or CPU (it's faster on the CPU).
'''

def permute(length: int, file, prev = None):
    if prev == None:
        prev = ""
    if len(prev) == length:
        return prev
    for i in range(ord('a'), ord('z') + 1):
        value = permute(length, file, prev + chr(i))
        if isinstance(value, str):
            file.write(value + ", ")

permute(int(input("size: ")), open(input("filename: ") + ".txt", "a+"))
print("done")
input()
