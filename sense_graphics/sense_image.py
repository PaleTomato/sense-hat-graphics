from __future__ import absolute_import
from sense_hat import SenseHat
from .image_layer import StaticLayer


class SenseImage(SenseHat):
    
    def __init__(self):
        
        SenseHat.__init__(self)
        self.layers = []
    
    def layer_static(self,image,update_display=True):
        """
        Adds a static image to the Sense Hat LED matrix. Multiple images can be
        stacked on top of each other (empty and semi-transparent areas of the
        image allow other images underneath to show through)
        
        If update_display is set to True, then the Sense Hat LED matrix will
        display the new image as soon as this method is run. Set to False if you
        wish to create a number of images in a stack, before displaying them
        simultaneously.
        """
        
        # Add the static image to the layer stack
        new_layer = StaticLayer(image)
        self.layers.append(new_layer)
        
        # If requested, update the display
        if update_display:
            self.show_image

    def show_image(self):
        """
        Displays the current layered image
        """
        pass
    
