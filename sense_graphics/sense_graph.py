from sense_hat import SenseHat
import time
import random

bar_colour = [255,0,0]

class SenseGraph(SenseHat):

    def add_bar(self,value):
        """
        Adds a new bar to the graph displayed on the Sense Hat LED display and
        moves the other bars across. value should be a percentage, expressed as
        a decimal.
        """

        empty = [0,0,0]

        pixels = self.get_pixels()

        # Rotate the list of elements around by 1
        pixels.append(pixels.pop(0))

        # Work out what values to set each new pixel to
        column = []
        value *= 8
        
        # Set the values used for each pixel of the bar
        while len(column) < 8:
            if value >= 1:
                pixel = bar_colour
                value -= 1
                
            elif value > 0:
                pixel = [round(channel * value) for channel in bar_colour]
                value = 0
                
            else:
                pixel = empty

            column.insert(0,pixel)

            
        # Replace the last column of the sense hat pixels with the new values
        new_pixel = 0
        for i in range(7, 64, 8):
            pixels[i] = column[new_pixel]
            new_pixel += 1

        self.set_pixels(pixels)


if __name__ == "__main__":

    sense = SenseGraph()
    sense.set_rotation(180)
    running = True
    try:
        while running:
            sense.add_bar(random.random())
            time.sleep(0.5)

    except KeyboardInterrupt:
        sense.clear()
