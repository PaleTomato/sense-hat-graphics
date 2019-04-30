from __future__ import absolute_import
from .image_layer import ImageLayer, ScrollingLayer, FlashingLayer


class LayerSet(object):
    """
    Class that is used to store and combine layer objects.

    Use this class to store the various layer objects, created from the
    ImageLayer and its sub-classes. Once layers have been added, it is possible
    to retrieve lists that combine the layers together. These lists can be
    shown on the Sense Hat using the SenseHat class' set_pixels() method.

    Methods:
    --------
    add_layer            - Add an extra layer to the image.
    add_effect_scrolling - Add a scrolling effect to a layer.
    add_effect_flashing  - Add a flashing effect to a layer.
    """

    def __init__(self, name="New Image"):
        """
        Initialise the class with a name.
        """

        self.layers = []
        self.name = name


    def __repr__(self):

        return self.__class__.__name__ + '("' + self.name + '")'


    def __getitem__(self, idx):
        """
        Return a list of rgb values at index idx.

        Overrides the built-in __getitem__ method to instead return a list of
        red, green and blue values (rgb) for the specified index. The list will
        have length of 64, and each element will itself be a 3 element list of
        integer values from 0 to 255. The 64 element list can be displayed on
        the Raspberry Pi Sense Hat using the set_pixels method of the SenseHat
        class.
        """

        frame = self._create_frame(idx)

        return frame.to_list()


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


    def _create_frame(self, frame_num):
        """
        Creates the specified frame from the stored layers.

        Return a Frame object for the specified frame number. The rgb values of
        the frame will vary depending on the animations set for the different
        layers that make up the frame.
        """

        this_layer_frames = []
        for layer in self.layers:
            this_layer_frames.append(layer[frame_num])


        return sum(this_layer_frames)


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


    def add_effect_scrolling(self, layer, direction='E', padding=0):
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

        if isinstance(layer, str):
            idx = self._get_layer_index(layer)

        elif isinstance(layer, int):
            idx = layer

        else:
            raise TypeError("Input 'layer' must be a string or integer")


        self.layers[idx] = ScrollingLayer(self.layers[idx], direction, padding)


    def add_effect_flashing(self, layer, pattern=[255, 0]):
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

        if isinstance(layer, str):
            idx = self._get_layer_index(layer)

        elif isinstance(layer, int):
            idx = layer

        else:
            raise TypeError("Input 'layer' must be a string or integer")


        self.layers[idx] = FlashingLayer(self.layers[idx], pattern)
