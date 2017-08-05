from __future__ import absolute_import
from sense_hat import SenseHat
from .image_layer import StaticLayer, ScrollingLayer, FlashingLayer
from .frame import Frame
import time


class SenseImage(SenseHat):
    
    def __init__(self):
        
        SenseHat.__init__(self)
        self.layers = []
    
    
    def add_layer_static(self, image_rgb, alpha, name="Static Layer 1"):
        """
        Adds a static image to the Sense Hat LED matrix.
        """
        
        # Add the static image to the layer stack
        self.layers.append(StaticLayer(image_rgb, alpha, name))
        
            
    def add_layer_scrolling(self, 
                            image_rgb,
                            alpha,
                            name="Moving Layer 1",
                            padding=0
                            ):
        """
        Adds an image to the Sense Hat LED matrix that scrolls from left to
        right.
        """
        
        # Add the scrolling layer to the layer stack 
        self.layers.append(ScrollingLayer(image_rgb, alpha, name, padding))

    
    def add_layer_flashing(self,
                        image_rgb,
                        alpha,
                        name="Flashing Layer 1",
                        flash_sequence=[255,0]
                        ):
         """
         Adds an image to the Sense Hat LED matrix that flashes in the specified
         flash squence. 255 indicates visible and 0 is not visible. Values in
         between are allowed and will make for semi-transparent images
         """
         
         self.layers.append(
            FlashingLayer(image_rgb, alpha, name, flash_sequence)
            )
            

    def set_pixels(self, pixel_list):
        
        if type(pixel_list) == Frame:
            pixel_list = pixel_list.to_list()
        
        SenseHat.set_pixels(self,pixel_list)
        
    
    def show_image_static(self):
        """
        Displays the current layered image as a static image, which is the first
        still in the animation
        """
        
        frame = self.create_frames(1)
        
        self.set_pixels(frame[0])
        
        
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
        
