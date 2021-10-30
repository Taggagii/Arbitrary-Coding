'''
Turn on, lock your computer, leave the room. After 10 seconds the camera will turn on and it will record and save any motion is detects until you come back and turn it off with the "`" key
'''


import cv2
import os, glob, time, ffmpeg
#cap = cv2.VideoCapture(0)
# use the main camera to pull video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("error opening file")


# initalize path's to save the frames with make up the final video
base_path = os.path.dirname(os.path.abspath(__file__))
temp_image_path = os.path.join(base_path, "temporary")
os.system("md temporary")

# perform the 10 second count down
start_time = time.time()
count = 10
while True:
    # countdown
    if time.time() - start_time > 1:
        print(count)
        count -= 1
        start_time = time.time()
        if count <= 0:
            break
            
# look at current frame and previous frame, if there are differences (removing camera static) will save a frame as the time.time() when the disturbance took place
ret, previous = cap.read()
while cap.isOpened():
    ret, frame = cap.read()
    diff = cv2.absdiff(previous, frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=4)
    contours, hiers = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours != []:
        print("motion detected")
        cv2.imwrite(f"{os.path.join(temp_image_path, str(time.time()))}.jpg", previous) 
        
               
    cv2.imshow('thing', previous)
    previous = frame
    # stops the while look when "`" is pressed
    if cv2.waitKey(60) == ord('`'):
        break

cv2.destroyAllWindows()

# get all the saved images
images = glob.glob(os.path.join(temp_image_path, "*.jpg"))

# initalize the size of the video using the first image
frame = cv2.imread(images[0])
height, width, layers = frame.shape

# initalize the video using the above size and a set name as time (name can be anything). 15 is the FPS, I just felt this was closest to my camera's intake with cv2
video = cv2.VideoWriter(f"{time.time()}.mp4", 0, 15, (width, height))

# goes through all the images and writes the frame
for image in images:
    video.write(cv2.imread(image))

cv2.destroyAllWindows()
video.release()

# destroy the content of the temp images (asks user Y or N) so next code can have empty folder
os.system("del temporary")
