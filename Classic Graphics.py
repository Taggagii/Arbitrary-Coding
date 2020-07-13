from PIL import Image, ImageTk
import imageio
import pynput
import tkinter
import math
import time
import os
import fitz
class Tetris:

    #initalization def holding all values needed globally throughout the code
    def __init__(self):
        #screen information
        fuck_color = (32, 14, 41)
        self.screen_dimensions = {'width' : 480, 'height' : 960}
        self.values = [[(32, 14, 41) for i in range(self.screen_dimensions['width'])] for i in range(self.screen_dimensions['height'])]
        for i in range(0, 480, 48):
            self.create_line((i, 0), (i, 959), (255, 255, 255))
        for i in range(0, 960, 48):
            self.create_line((0, i), (480, i), (255, 255, 255))

        
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window,
                                     width = self.screen_dimensions['width'],
                                     height = self.screen_dimensions['height'])
        self.canvas.pack()
        
        
        #player information
        self.shape = 1 #PLUS SIGN ALTERABLE FOR TESTING ONLY — SET TO RANDOMIZER FOR GAME
        self.player_location = [48, 672]
        self.min_x, self.min_y, self.max_x, self.max_y = 0, 0, 0, 0
        self.rotation = 1
        self.rotate_right, self.rotate_left = False, False
        self.player_action_detected = False
        
        #program status/information
        self.leave = False
        self.left_clicking = False
        self.right_clicking = False
        self.right, self.left, self.up, self.down = False, False, False, False
        self.left_mouse_places = []
        self.right_mouse_place = []
        self.images = []

        #user interaction setup
        self.mouse_listener = pynput.mouse.Listener(on_click = self.on_click)
        self.keyboard_listener = pynput.keyboard.Listener(on_press = self.on_press, on_release = self.on_release)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.window.bind('<Motion>', self.motion)

        #pausing to prevent that weird error
        time.sleep(1)

        #running the main program loop
        self.main_loop()

        #closing all interfaces
        self.window.destroy()
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

        #saves the frames as a video
        print('saving...')
        imageio.mimsave('recording.mp4', self.images ,fps=2, macro_block_size = 100)
        print('saved')



    #main loop which runs all the other defs
    def main_loop(self):
        while not self.leave:
            self.update_screen(save = False)
            self.move_player()
            #self.draw_on_click(save = True) #if you want to enable drawing


    #start of the screen manipulation defs — defs that edit and show individual pixels on the screen
    
    def update_screen(self, sleep_time = 0, save = True):
        screen = Image.new('RGB', ([i for i in self.screen_dimensions.values()]))
        screen.putdata([value for sublist in self.values for value in sublist])
        if save: self.images.append(screen)
        screen = ImageTk.PhotoImage(screen)
        self.canvas.create_image(self.screen_dimensions['width']//2, self.screen_dimensions['height']//2, image = screen)
        self.window.update()
        time.sleep(sleep_time)


    def change_screen_value(self, location, color = (0, 0, 0)):
        if isinstance(location, list) or isinstance(location, set):
            for place in location:
                try:
                    self.values[self.screen_dimensions['height'] - place[1] - 1][place[0]+3] = color
                except:
                    continue
        else:
            try:
                self.values[self.screen_dimensions['height'] - location[1] - 1][location[0]+3] = color
            except:
                return 0


    #start of the creation defs — defs that manipulate the baseline defs to make objects and images


    def create_dot(self, location, radius = 2, color = (0, 0, 0), fill = True):
        x1, y1 = location
        points = set()
        radius = int(radius)
        for x in range(x1 - radius, x1 + radius):
            radican = round(math.sqrt(radius**2 - x1**2 + 2*x1*x - x**2))
            points.add((x, radican + y1))
            points.add((x, -radican + y1))
        for y in range(y1 - radius, y1 + radius):
            radican = round(math.sqrt(radius**2 - y1**2 + 2*y1*y - y**2))
            points.add((radican + x1, y))
            points.add((-radican + x1, y))
        if fill:
            points = list(points)
            points.sort()
            for i in range(1, len(points)):
                self.create_straight_line(points[i], points[i-1], color)
        else:
                self.change_screen_value(points)
                
        
    def create_straight_line(self, point_one, point_two, color = (0, 0, 0), size = 1):
        run, rise = point_two[0] - point_one[0], point_two[1] - point_one[1]
        right = 1 if run > 0 else -1 if run < 0 else 0
        up = 1 if rise > 0 else -1 if rise < 0 else 0
        if abs(right) - abs(up) == 0: return run, rise, right, up
        x, y = point_one
        while (x, y) != point_two:
            if size == 1:
                self.change_screen_value((x, y), color)
            if size > 1:
                self.create_dot((x, y), size, color)
            x += right
            y += up


    def create_line(self, point_one, point_two, color = (0, 0, 0), size = 1):
        if point_one == point_two:
            if size == 1:
                self.change_screen_value(point_one, color)
            if size > 1:
                self.create_dot(point_one, size, color)
            return 0
        point_one, point_two = sorted([point_one, point_two])
        try: run, rise, right, up = self.create_straight_line(point_one, point_two, color, size)
        except: return 0
        m = rise/run
        x1, y1 = point_one
        b = y1 - (m * x1)
        if run >= rise:
            end_x = point_two[0]
            while x1 != end_x:
                x1 += right
                y1 = round((m * x1) + b)
                if size == 1: self.change_screen_value((x1, y1), color)
                if size > 1: self.create_dot((x1, y1), size, color)
            return 1
        if run < rise:
            end_y = point_two[1]
            while y1 != end_y:
                y1 += up
                x1 = round((y1 - b)/m)
                if size == 1: self.change_screen_value((x1, y1), color)
                if size > 1: self.create_dot((x1, y1), size, color)
            return 1


    def create_image(self, image, location, as_png = False):
        if isinstance(image, str):
            image = Image.open(image)
        image_width, image_height = image.size
        image = list(image.getdata())
        x, y = location
        y += image_height
        hold_x = x
        end_x = x + image_width
        for pixel in image:
            if as_png and pixel != (255, 255, 255, 255) and pixel != (255, 255, 255):
                self.change_screen_value((x, y), pixel)
            x += 1
            if x == end_x:
                x = hold_x
                y -= 1


    def create_square(self, location, color = (0, 0, 0), scale_factor = 48, fill = False, border = False):
        start_x, start_y = location[0]-scale_factor//2, location[1]+scale_factor//2
        end_x, end_y = location[0]+scale_factor//2, location[1]-scale_factor//2
##        start_x, start_y = location
##        end_x, end_y = location[0] + int(10 * scale_factor), location[1] - int(10 * scale_factor)
        if fill:
            for y in range(end_y, start_y):
                self.create_straight_line((start_x, y), (end_x, y), color)
        if not fill or border:
            if border: color = (color[0] - 120, color[1] - 120, color[2] - 120)
            self.create_straight_line((start_x, start_y), (start_x, end_y), color)
            self.create_straight_line((start_x, end_y), (end_x, end_y), color)
            self.create_straight_line((end_x, end_y), (end_x, start_y), color)
            self.create_straight_line((end_x, start_y), (start_x, start_y), color)



    def create_shape(self, location, shape_number = 1, rotation = 1):
##        penis = 48
##        location = ((penis*((location[0]//penis))), (penis*((location[1]//penis))))
        #print(location, 'location for create shape')
        scale_factor = 48 
        shapes = {
            1: ([(scale_factor//2, int(-scale_factor*1.5)), (scale_factor//2, -scale_factor//2), (-scale_factor//2, -scale_factor//2), (-scale_factor//2, scale_factor//2)], (153, 255, 51)), 
            2 : ([(-scale_factor//2, -int(scale_factor*1.5)), (-scale_factor//2, -scale_factor//2), (scale_factor//2, -scale_factor//2), (scale_factor//2, scale_factor//2)], (255, 0, 0)),
            3 : ([(-scale_factor//2, -int(scale_factor*1.5)), (-scale_factor//2, -scale_factor//2), (-scale_factor//2, scale_factor//2), (-scale_factor//2, int(scale_factor*1.5))], (0, 255, 255)),
            4 : ([(-scale_factor//2, -scale_factor//2), (-scale_factor//2, scale_factor//2), (scale_factor//2, scale_factor//2), (scale_factor//2, -scale_factor//2)], (255, 255, 0)),
            5 : ([(-scale_factor//2, -int(scale_factor//2)), (-scale_factor//2, scale_factor//2), (-scale_factor//2 + scale_factor, scale_factor//2), (-scale_factor//2, int(scale_factor*1.5))], (255, 0, 255)),
            6 : ([(scale_factor//2, -scale_factor//2), (-scale_factor//2, -scale_factor//2), (-scale_factor//2, scale_factor//2), (-scale_factor//2, int(scale_factor*1.5))], (255, 178, 102)),
            7 : ([(-scale_factor//2, -scale_factor//2), (scale_factor//2, -scale_factor//2), (scale_factor//2, scale_factor//2), (scale_factor//2, int(scale_factor*1.5))], (0, 0, 255))
                }
        shape, color = shapes[shape_number]
        for i in range(len(shape)):
#            x, y = (36*(1 + (location[0]//36))), (36*(1 + (location[1]//36)))
            x, y = self.rotate(shape[i], rotation)
##            print(x, y, i)
            x += location[0]
            y += location[1]
            shape[i] = (x, y)
            
##        print(shape)
        self.min_x, self.max_x = min(shape)[0]%480, max(shape)[0]%480
        shape_reversed = [(i[1], i[0]) for i in shape]
        self.min_y, self.max_y = min(shape_reversed)[0]%960, max(shape_reversed)[0]%960
##        print(self.min_x, self.min_y, self.max_x, self.max_y)
        for placement in shape:
            self.create_square(placement, color, scale_factor, True, True)


    

        
    #start of user input defs — defs that allow the user to interact with the program

    def on_click(self, x, y, button, pressed):
        if str(button) == 'Button.left':
            self.left_clicking = pressed
            self.left_mouse_places = []
        elif str(button) == 'Button.right':
            self.right_clicking = pressed
            self.right_mouse_places = []


    def motion(self, event):
        if self.left_clicking and 0 < event.x < self.screen_dimensions['width'] - 3 and 0 < event.y < self.screen_dimensions['height'] - 1:
            self.left_mouse_places.append((event.x - 4, self.screen_dimensions['height'] - event.y))
        elif self.right_clicking and 0 < event.x < self.screen_dimensions['width'] - 3 and 0 < event.y < self.screen_dimensions['height'] - 1:
            self.right_mouse_places.append((event.x - 4, self.screen_dimensions['height'] - event.y))


    def on_press(self, key):
        if not self.player_action_detected:
            if key == pynput.keyboard.Key.esc:
                self.leave = True
                return False
            if key == pynput.keyboard.Key.right:
                self.right = True
                self.player_action_detected = True
            if key == pynput.keyboard.Key.left:
                self.left = True
                self.player_action_detected = True
            if key == pynput.keyboard.Key.up:
                self.up = True
                self.player_action_detected = True
            if key == pynput.keyboard.Key.down:
                self.down = True
                self.player_action_detected = True
            if str(key).lower() == "'a'":
                self.rotate_left = True
                self.player_action_detected = True
            if str(key).lower() == "'s'":
                self.rotate_right = True
                self.player_action_detected = True
            if str(key) == "'='":
                self.rotation = 1
                self.shape += 1
                self.shape %= 8
                if self.shape == 0: self.shape = 1
                self.player_action_detected = True
            if str(key) == "'-'":
                self.rotation = 1
                self.shape -= 1
                self.shape %= 8
                if self.shape == 0: self.shape = 7
                self.player_action_detected = True
            


    def on_release(self, key):
        if key == pynput.keyboard.Key.right:
            self.right = False
        if key == pynput.keyboard.Key.left:
            self.left = False
        if key == pynput.keyboard.Key.up:
            self.up = False
        if key == pynput.keyboard.Key.down:
            self.down = False
        if str(key).lower() == "'a'":
            self.rotate_left = False
        if str(key).lower() == "'s'":
            self.rotate_right = False


    def draw_on_click(self, save = False):
        if self.left_clicking:
            if len(self.left_mouse_places) > 1:
                for i in range(1, len(self.left_mouse_places)):
                    try:
                        self.create_line(self.left_mouse_places[i-1], self.left_mouse_places[i], (0, 0, 0), 2)
                    except:
                        continue
                self.left_mouse_places = [self.left_mouse_places[-1]]
        elif self.right_clicking:
            if len(self.right_mouse_places) > 1:
                for i in range(1, len(self.right_mouse_places)):
                    try:
                        self.create_line(self.right_mouse_places[i - 1], self.right_mouse_places[i], (255, 255, 255), 7)
                    except:
                        continue
                self.right_mouse_places = [self.right_mouse_places[-1]]
        self.update_screen(save = save)


    def move_player(self):
        speed = 48
        if self.player_action_detected:
            if self.right and self.max_x < 456:
                self.player_location[0] += speed
            if self.left and self.min_x > 24:
                self.player_location[0] -= speed
            if self.up and self.max_y < 936:
                self.player_location[1] += speed
            if self.down and self.min_y > 216:
                self.player_location[1] -= speed
            if self.rotate_right:
                self.rotation += 1
                self.rotation %= 5
                if self.rotation == 0: self.rotation = 1
            if self.rotate_left:
                self.rotation -= 1
                self.rotation %= 5
                if self.rotation == 0: self.rotation = 4
            self.values = [[(32, 14, 41) for i in range(self.screen_dimensions['width'])] for i in range(self.screen_dimensions['height'])]
            for i in range(0, 480, 48):
                self.create_line((i, 0), (i, 950), (255, 255, 255))
            for i in range(0, 960, 48):
                self.create_line((0, i), (480, i), (255, 255, 255))
            self.create_shape(self.player_location, self.shape, self.rotation)
            self.update_screen(save = True)
            self.player_action_detected = False



    #start of alteration defs — defs that alter points to perform functions

    def rotate(self, location, rotation = 1):
        
##        penis = 24
##        location = ((penis*(1 + (location[0]//penis))), (penis*(1 + (location[1]//penis))))
        if rotation == 1: return location
        if rotation == 2: return (location[1], self.screen_dimensions['height'] - location[0])
        if rotation == 3: return (-location[0], self.screen_dimensions['height'] - location[1])
        if rotation == 4: return (-location[1], location[0])


#self.values[self.screen_dimensions['height'] - location[1] - 1][location[0]+3] = color
        
if __name__ == '__main__':
    tetris = Tetris()
    
