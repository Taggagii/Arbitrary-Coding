
#sorts a list into smallest-to-largest

def insertion_sort(values):
    # create the new list for all the sorted values
    output = []
    # go through all the values...
    for i in values:
        # and insert them into output, so that output stays sorted
        #    (insert() is doing the the sorting, this is really just a cover)
        output = insert(i, output)
    return output

# insert fuction that inserts the "value" into the "sorted_list"
#    so that it remains sorted
def insert(value, sorted_list):
    # if the sorted list is empty then to keep it sorted
    #    you just put the value inside it
    if sorted_list == []:
        return [value]
    # go through all the values in the sorted list and...
    for i in range(len(sorted_list)):
        # if you reach the spot your value goes...
        #   (if you put 4 into [1, 2, 3, 5] then you insert
        #    once you reach 5, or, when you reach a value that's
        #    larger than 4)
        if sorted_list[i] >= value:
            # insert it into the list
            return sorted_list[:i] + [value] + sorted_list[i:]
    # if you never find a spot to put it, stick it on the end
    #   (if there is no value that is larger then this is the largest so put it
    #    at the end)
    return sorted_list + [value]
        

