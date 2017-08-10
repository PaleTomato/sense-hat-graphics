from __future__ import absolute_import
from sense_hat import SenseHat
from .image_layer import ImageLayer, ScrollingLayer, FlashingLayer
from .frame import Frame
import time


class SenseImage(SenseHat):
    
    def __init__(self):
        
        SenseHat.__init__(self)
        self.layers = []
    
    
    def _get_layer_index(self, layer_name):
        """
        Get the index of the layer with name layer_name. Outputs the index of
        the layer if a layer with that name exists already. If the layer does
        not exist then False is outputted
        """
        
        for idx in range(len(self.layers)):
            if self.layers[idx].get_name() == layer_name:
                return idx
        
        return False
        
    
    def add_layer(self, rgb, alpha, name="New Layer"):
        """
        Adds a new image layer to the Sense Hat LED matrix.
        """
        
        if self._get_layer_index(name):
            raise ValueError("A layer with name '%s' already exists" % name)
            
        
        self.layers.append(ImageLayer(rgb, alpha, name))
        
            
    def add_effect_scrolling(self, layer, direction = 'E', padding=0):
        """
        Adds a scrolling effect to the specified layer. Input layer can be
        either an integer layer index, or the name of the layer, i.e. a string.
        """
        
        if type(layer) == str:
            idx = self._get_layer_index(layer)
        
        elif type(layer) == int:
            idx = layer
            
        else:
            raise TypeError("Input 'layer' must be a string or integer")
        
        
        self.layers[idx] = ScrollingLayer(self.layers[idx], direction, padding)

    
    def add_effect_flashing(self, layer, flash_sequence=[255,0]):
        """
        Adds a flashing effect to the specified layer. 
        """
        
        if type(layer) == str:
            idx = self._get_layer_index(layer)
        
        elif type(layer) == int:
            idx = layer
            
        else:
            raise TypeError("Input 'layer' must be a string or integer")
            
        
        self.layers[idx] = FlashingLayer(self.layers[idx], flash_sequence)

            
    def set_pixels(self, pixel_list):
        
        if type(pixel_list) == Frame:
            pixel_list = pixel_list.to_list()
        
        SenseHat.set_pixels(self,pixel_list)
        
    
    def show_image_static(self, frame_num=0):
        """
        Displays the current layered image as a static image. Input frame_num is
        the index of the frame to show, which is the first
        still in the animation by default (frame 0)
        """
        
        frame = self.create_frames(frame_num + 1)
        
        self.set_pixels(frame[frame_num])
        
        
    def show_image_dynamic(self, scroll_speed=0.5, total_time=10):
        """
        Displays the current layered image as an animated image
        """
        num_frames = int(total_time/scroll_speed)
        
        frames = self.create_frames(num_frames)
        
        
        for frame in frames:
            
            self.set_pixels(frame)
            time.sleep(scroll_speed)
            
            
    def create_frames(self, num_frames):
        """
        Creates the specified number of frames by looping through the layers as
        appropriate
        """
        
        frames = []
        
        for i in range(num_frames):
            
            # Make a list of all the layered frames in this frame
            this_layer_frames = []
            for layer in self.layers:
                this_layer_frames.append(layer.get_frame(i))
            
            
            # Combine all the individual layered frames together
            frames.append(sum(this_layer_frames))
        
        return frames
        
