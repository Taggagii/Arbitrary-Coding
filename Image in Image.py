from PIL import Image
import pyscreenshot as ss
#print([i for i in globals() if globals()[i] is value]) just a thing
indexes = [0]
#one = ss.grab((200, 200, 700, 700))
#two = ss.grab((400, 400, 425, 425))
one = Image.open('imageone.png')
two = Image.open('imagetwo.png')
widthone, heightone = one.size
widthtwo, heighttwo = two.size
one.show()
two.show()
one = list(one.getdata())
two = list(two.getdata())
while indexes != []:
    
    ##one = ss.grab((0, 0, 200, 200))
    ##two = ss.grab((100, 100, 200, 200))

    #one.show()

    holder = one
    #if two in one
    def make_matrix(values, row_length):
        output = []
        for i in range(0, len(values), row_length):
            output.append(values[i:i+row_length])
        return output

    def bias_matrix(values, row_length):
        output = []
        for i in range(row_length, len(values)):
            output.append(values[i-row_length:i])
        return output

    def is_in(two, one):
        row_length = widthtwo
        for i in range(0, len(one), row_length):
            #print('\n', one[i:i+row_length], two)
            if one[i:i+row_length] == two:
                return True, i

    def change_color(data, indexes, row_length):
        output = []
        counter = 0
        for i in range(len(data)):
            if i in indexes or counter > 0:
                output.append((data[i][0], 0, data[i][2]))
                counter += 1
                if counter == row_length:
                    counter = 0
                continue
            output.append(data[i])
        return output
            
    two = (make_matrix(two, widthtwo))
    one = bias_matrix(one, widthtwo)
    indexes = []
    for i in two:
        if i in one:
            indexes.append(one.index(i))
    thing = ([one[i] for i in indexes])
    thing = (change_color(holder, indexes, widthtwo))
    new = Image.new('RGBA', (widthone, heightone))
    new.putdata(thing)
    one = thing
    print(indexes)
new = Image.new('RGBA', (widthone, heightone))
new.putdata(one)
new.show()


