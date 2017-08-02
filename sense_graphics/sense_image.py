from __future__ import absolute_import
from sense_hat import SenseHat
from .image_layer import StaticLayer, ScrollingLayer
import time


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
            
    def layer_scrolling(self, image, name="Moving Layer 1"):
	
        self.layers.append(ScrollingLayer(image, name))


    def show_image_dynamic(self, scroll_speed=0.5, total_time=10):
        """
        Displays the current layered image as an animated image
        """
        num_frames = int(total_time/scroll_speed)
        
        frames = self.create_frames(num_frames)
        
        
        for frame in frames:
            
            self.set_pixels(frame)
            time.sleep(scroll_speed)
            
            
            
    def show_image_static(self):
        """
        Displays the current layered image as a static image, which is the first
        still in the animation
        """
        
        frame = self.create_frames(1)
        
        self.set_pixels(frame[0])
        
        
    def create_frames(self, num_frames):
        """
        Creates the specified number of frames by looping through the layers as
        appropriate
        """
        
        # Create an empty set of frames to begin with
        empty_frame = [[0,0,0]] * 64
        frames = [empty_frame] * num_frames
        
        # Loop through each layer
        for layer in self.layers:
            frame_num = 0
            layer_idx = 0
            
            # Get the stills for this layer
            layer_stills = layer.get_frames()
            
            # Apply the each still of the layer to the appropriate frame
            while frame_num < num_frames:
                if layer_idx >= len(layer_stills):
                    layer_idx = 0
                    
                frames[frame_num] = layer_stills[layer_idx]
                frame_num += 1
                layer_idx += 1
            
        return frames
