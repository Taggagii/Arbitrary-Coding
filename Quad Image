#takes a screenshot and then does super easy crap until to make it into four of the same image
#it's sorta pointless but boredom doesn't care
#can be altered to do other things to the image (obviously)

from PIL import Image
import pyscreenshot as ss
image = ss.grab()
#image.show()
magic = list(image.getdata())
#magic.reverse()
newthing = []
holder = []
counter = 0
count = False
for thing in magic:
    counter += 1
    if counter % 2 == 0:
        count = not count
    if count:
        holder.append(thing)
    else:
        newthing.append(thing)

for thing in holder:
    newthing.append(thing)
newimage = Image.new(image.mode, image.size)
newimage.putdata(newthing)
newimage.show()
