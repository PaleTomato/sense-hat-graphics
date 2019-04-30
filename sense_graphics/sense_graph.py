import random
import time

from sense_hat import SenseHat

BAR_COLOUR = [255, 0, 0]

class SenseGraph(SenseHat):
    """
    Extension of the Sense Hat class, with basic plotting capability.

    The SenseGraph class is a subclass of the SenseHat class, and therefore
    retains the SenseHat methods that enable it to take readings from the Sense
    Hat's sensors, and display text and images on the LED matrix. The
    SenseGraph builds on this functionality by having the ability to display
    a simple bar graph on the LED matrix.

    Methods:
    --------
    add_bar   - Add an extra bar to the graph on the SenseHat.
    """

    def add_bar(self, value):
        """
        Add a new bar to the graph displayed on the LED matrix.

        Update the graph shown on the Sense Hat LED matrix with a new bar on
        the right-hand side. All existing bars will be shifted one place to the
        left.

        Inputs:
        -------
        value - Value for the bar to display. This should be a percentage,
                expressed as a decimal number between 0 and 1. The height of
                the bar will reflect the inputted value.
        """

        empty = [0, 0, 0]

        pixels = self.get_pixels()

        # Rotate the list of elements around by 1
        pixels.append(pixels.pop(0))

        # Work out what values to set each new pixel to
        column = []
        value *= 8

        # Set the values used for each pixel of the bar
        while len(column) < 8:
            if value >= 1:
                pixel = BAR_COLOUR
                value -= 1

            elif value > 0:
                pixel = [round(channel * value) for channel in BAR_COLOUR]
                value = 0

            else:
                pixel = empty

            column.insert(0, pixel)


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
