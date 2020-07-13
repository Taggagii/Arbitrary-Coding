from PIL import Image, ImageTk
import imageio, pynput, tkinter, math, time
class Tetris:

    #initalization def holding all values needed globally throughout the code
    def __init__(self):
        #screen information
        self.screen_dimensions = {'width' : 500, 'height' : 500}
        self.values = [[(255, 255, 255) for i in range(self.screen_dimensions['width'])] for i in range(self.screen_dimensions['height'])]
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window,
                                     width = self.screen_dimensions['width'],
                                     height = self.screen_dimensions['height'])
        self.canvas.pack()
        
        
        #player information
        self.player_location = {'x' : self.screen_dimensions['width']//2,
                                'y' : self.screen_dimensions['height']//2}
        
        #program status/information
        self.leave = False
        self.clicking = False
        self.mouse_places = []
        self.images = []

        #user interaction setup
        self.mouse_listener = pynput.mouse.Listener(on_click = self.on_click)
        self.keyboard_listener = pynput.keyboard.Listener(on_press = self.on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.window.bind('<Motion>', self.motion)

        #pausing to prevent that weird error
        time.sleep(1)

        #running the main program loop
        self.create_image('fuckimage.png', (255, 255), as_png = True)
        self.main_loop()

        #closing all interfaces
        self.window.destroy()
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        

    #main loop which runs all the other defs
    def main_loop(self):
        while not self.leave:
            self.update_screen(save = False)
            if len(self.mouse_places) > 1:
                for i in range(1, len(self.mouse_places)):
                    self.create_line(self.mouse_places[i-1], self.mouse_places[i])
                self.mouse_places = [self.mouse_places[-1]]


    #start of the screen manipulation defs — defs that edit and show individual pixels on the screen
    
    def update_screen(self, save = True):
        screen = Image.new('RGB', ([i for i in self.screen_dimensions.values()]))
        screen.putdata([value for sublist in self.values for value in sublist])
        if save: self.images.append(screen)
        screen = ImageTk.PhotoImage(screen)
        self.canvas.create_image(self.screen_dimensions['width']//2, self.screen_dimensions['height']//2, image = screen)
        self.window.update()


    def change_screen_value(self, location, color = (0, 0, 0)):
        if isinstance(location, list):
            for place in location:
                self.values[self.screen_dimensions['height'] - place[1] - 1][place[0]+3] = color
        else:
            self.values[self.screen_dimensions['height'] - location[1] - 1][location[0]+3] = color


    #start of the creation defs — defs that manipulate the baseline defs to make objects and images
    
    def create_straight_line(self, point_one, point_two, color = (0, 0, 0)):
        run, rise = point_two[0] - point_one[0], point_two[1] - point_one[1]
        right = 1 if run > 0 else -1 if run < 0 else 0
        up = 1 if rise > 0 else -1 if rise < 0 else 0
        if abs(right) - abs(up) == 0: return run, rise, right, up
        x, y = point_one
        while (x, y) != point_two:
            self.change_screen_value((x, y), color)
            x += right
            y += up


    def create_line(self, point_one, point_two, color = (0, 0, 0)):
        point_one, point_two = sorted([point_one, point_two])
        try: run, rise, right, up = self.create_straight_line(point_one, point_two, color)
        except: return 0
        m = rise/run
        x1, y1 = point_one
        b = y1 - (m * x1)
        if run > rise:
            end_x = point_two[0]
            while x1 != end_x:
                x1 += right
                y1 = round((m * x1) + b)
                self.change_screen_value((x1, y1), color)
            return 1
        if run < rise:
            end_y = point_two[1]
            while y1 != end_y:
                y1 += up
                x1 = round((y1 - b)/m)
                self.change_screen_value((x1, y1), color)
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


    #start of user input defs — defs that allow the user to interact with the program

    def on_click(self, x, y, button, pressed):
        self.clicking = pressed
        self.mouse_places = []


    def motion(self, event):
        if self.clicking and 0 < event.x < self.screen_dimensions['width'] - 3 and 0 < event.y < self.screen_dimensions['height'] - 1:
            self.mouse_places.append((event.x, self.screen_dimensions['height'] - event.y))


    def on_press(self, key):
        if key == pynput.keyboard.Key.esc:
            self.leave = True
            return False
    
                
        
            

    

        
if __name__ == '__main__':
    tetris = Tetris()
    
