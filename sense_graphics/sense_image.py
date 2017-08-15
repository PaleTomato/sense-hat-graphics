from __future__ import absolute_import
from sense_hat import SenseHat
from .image_layer import ImageLayer, ScrollingLayer, FlashingLayer
from .frame import Frame
import time


class SenseImage(SenseHat):
    """
    Extension of the SenseHat class with complex image display options
    
    The SenseImage class is a subclass of the SenseHat class, and therefore
    retains the SenseHat methods that enable it to take readings from the Sense
    Hat's sensors, and display text and images on the LED matrix. The
    SenseImage class builds on this by having the ability to build up an image
    from a number of 'layers.' These layers can also be animated, for example
    scrolling across the screen or flashing on and off.
    
    Methods:
    --------
    add_layer            - Add an extra layer to the image.
    add_effect_scrolling - Add a scrolling effect to a layer.
    add_effect_flashing  - Add a flashing effect to a layer.
    show_image_static    - Display the layers as a still image.
    show_image_dynamic   - Display the layers animated in their specified ways.
    """
    
    def __init__(self):
        """
        Initialise the Sense Hat.
        
        Extends the SenseHat class by setting an additional parameter for
        storing layers
        """
        
        SenseHat.__init__(self)
        self.layers = []
    
    
    def _get_layer_index(self, layer_name):
        """
        Get the index of the layer with name layer_name.
        
        Returns the index of the layer if a layer with the name layer_name
        exists already. If the layer does not exist then False is outputted.
        """
        
        for idx in range(len(self.layers)):
            if self.layers[idx].get_name() == layer_name:
                return idx
        
        return False
        
    
    def add_layer(self, rgb, alpha, name="New Layer"):
        """
        Add a new image layer to the Sense Hat LED matrix.
        
        Append a layer to the list of layers. The new layer will always appear
        underneath any previously created layers. The layer will not be
        immediately displayed on the LED matrix; use the show_image_ methods to
        display any inputted layers.
        
        Inputs:
        -------
        rgb   - 64-element list, where each element is a 3-element list
                representing the red, green and blue (rgb) values. The values
                in each sub-list should be integers between 0 and 255.
        alpha - 64 element list of integers between 0 and 255. A value of 0
                means that the pixel will be treated as invisible, and 255
                means the pixel is fully opaque.
        name  - The name of this layer. The name should be unique to the list
                of layers.
        """
        
        if self._get_layer_index(name):
            raise ValueError("A layer with name '%s' already exists" % name)
            
        
        self.layers.append(ImageLayer(rgb, alpha, name))
        
            
    def add_effect_scrolling(self, layer, direction = 'E', padding=0):
        """
        Add a scrolling effect to the specified layer.
        
        Modifies the specified layer by allowing it to scroll across the LED
        matrix when displayed using the show_image_dynamic method. The scroll
        direction can be specified as well as padding applied when scrolling.
        
        Inputs:
        -------
        layer     - The image layer to apply the animation to. You can specify
                    either the name of the layer or its index in self.layers.
                    Note that it is possible to apply multiple effects to a
                    single layer.
        direction - The direction in which to scroll. Use 'N', 'S', 'E' or 'W'
                    to scroll north (up) south (down) east (left) or west
                    (right) respectively.
        padding   - The number of blank pixels to append to the image when
                    scrolling. A padding of 8 would mean that your image will
                    scroll entirely off the display before it reappears on the
                    other side.
        """
        
        if type(layer) == str:
            idx = self._get_layer_index(layer)
        
        elif type(layer) == int:
            idx = layer
            
        else:
            raise TypeError("Input 'layer' must be a string or integer")
        
        
        self.layers[idx] = ScrollingLayer(self.layers[idx], direction, padding)

    
    def add_effect_flashing(self, layer, pattern=[255,0]):
        """
        Add a flashing effect to the specified layer.
        
        Modifies the specified layer by allowing it to flash (or fade in and
        out) when displayed using the show_image_dynamic method. The speed at
        which it flashes or fades can be specified.
        
        Inputs:
        -------
        layer     - The image layer to apply the animation to. You can specify
                    either the name of the layer or its index in self.layers.
                    Note that it is possible to apply multiple effects to a
                    single layer.
        pattern   - List of integer values from 0 to 255. In a similar way to
                    an image layer's alpha values, a value of 0 will make the
                    image completely invisible, and a value of 255 opaque. By
                    setting values in between these extremes you can make an
                    image fade. The pattern will repeat itself when using the
                    show_image_ methods.
        """
        
        if type(layer) == str:
            idx = self._get_layer_index(layer)
        
        elif type(layer) == int:
            idx = layer
            
        else:
            raise TypeError("Input 'layer' must be a string or integer")
            
        
        self.layers[idx] = FlashingLayer(self.layers[idx], pattern)

            
    def set_pixels(self, pixel_list):
        """
        Extends the SenseHat method by allowing displaying of Frame objects.
        """
        
        if type(pixel_list) == Frame:
            pixel_list = pixel_list.to_list()
        
        SenseHat.set_pixels(self,pixel_list)
        
    
    def show_image_static(self, frame_num=0):
        """
        Display the current layered image as a static image.
        
        Use this method to display your layers together as a static image. It
        is possible to specify a frame number from the dynamic image to use.
        
        Inputs:
        -------
        frame_num - The number of the frame from the show_image_dynamic method
                    to display. The default is 0 i.e. the first frame
        """
        
        frame = self._create_frames(frame_num + 1)
        
        self.set_pixels(frame[frame_num])
        
        
    def show_image_dynamic(self, scroll_speed=0.5, total_time=10):
        """
        Display the current layered image as an animated image.
        
        Use this method to display your layers together as an animated image.
        Any behaviours set using the add_effect_ methods will function in the
        way that they have been set.
        
        Inputs:
        -------
        scroll_speed  - The speed of the animation in frames per second.
        total_time    - The total time to display the animation, in seconds.
        """
        
        num_frames = int(total_time/scroll_speed)
        
        frames = self._create_frames(num_frames)
        
        
        for frame in frames:
            
            self.set_pixels(frame)
            time.sleep(scroll_speed)
            
            
    def _create_frames(self, num_frames):
        """
        Creates the specified number of frames from the stored layers.
        
        Return a list of Frame objects the length of the inputted number of
        frames. The rgb values of the frames will vary depending on the
        animations set for the different layers that make up each frame.
        """
        
        frames = []
        
        for i in range(num_frames):
            
            # Make a list of all the layered frames in this frame
            this_layer_frames = []
            for layer in self.layers:
                this_layer_frames.append(layer[i])
            
            
            # Combine all the individual layered frames together
            frames.append(sum(this_layer_frames))
        
        return frames
        
