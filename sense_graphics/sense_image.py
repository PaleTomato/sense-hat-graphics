from __future__ import absolute_import
import time

from sense_hat import SenseHat


class SenseImage(SenseHat):
    """
    Extension of the SenseHat class that can display animated graphics.

    The SenseImage class is a subclass of the SenseHat class, and therefore
    retains the SenseHat methods that enable it to take readings from the Sense
    Hat's sensors, and display text and images on the LED matrix. The
    SenseImage class builds on this by having the ability to display a sequence
    of images as an animation, built using the LayerSet class.

    Methods:
    --------
    set_pixels_dynamic   - Display a LayerSet object with animations.
    """

    def set_pixels_dynamic(self, layer_set, scroll_speed=0.5, total_time=10):
        """
        Display a LayerSet object with animations

        Use this method to display a LayerSet object as an animated image. Any
        behaviours set using its add_effect_ methods will function in the way
        that they have been set.

        Inputs:
        -------
        layer_set     - A LayerSet object
        scroll_speed  - The speed of the animation in frames per second.
        total_time    - The total time to display the animation, in seconds.
        """

        num_frames = int(total_time/scroll_speed)

        for frame_num in range(num_frames):

            self.set_pixels(layer_set[frame_num])
            time.sleep(scroll_speed)
            