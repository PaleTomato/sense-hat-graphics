from __future__ import absolute_import
import numpy as np
from .frame import Frame

class ImageLayer(object):
    def __init__(self, rgb, alpha, name="Layer 1"):
        
        # Convert rgb and alpha to numpy arrays
        rgb   = np.array(rgb, dtype = np.uint8)
        alpha = np.array(alpha, dtype = np.uint8)
        
        # Reshape from 64x3 to 8x8x3
        self.rgb   = rgb.reshape(8,8,3)
        self.alpha = alpha.reshape(8,8)

        self.name  = name
        
        
        
    def get_frame(self, frame_num=0):
        """
        Returns the frame frame_num of the layer. For a static layer this will
        always be the same as the main image layer. Frame 0 is the starting
        frame.
        """
        
        return Frame(self.rgb,self.alpha)
        
        
    def get_name(self):
        
        return self.name
        
    
    def __len__(self):
        """
        Returns number of frames for this image layer
        """
        return len(self.frames)
    
    
    def __iter__(self):
        return self


    def __next__(self):
        if self.current_frame >= len(self.frames):
            raise StopIteration
        else:
            self.current_frame += 1
            return self.frames[self.current_frame]



class AnimatedLayer(ImageLayer):
    """
    Class for an animated layer. All animated layers should be subclassed off
    this class.
    """
    
    def __init__(self, image_layer):
        
        self.image_layer = image_layer
    
    
    def get_frame(self, frame_num=0):
        
        return self.image_layer.get_frame()
        
        
    def get_name(self):
        
        return self.image_layer.get_name()
        

class ScrollingLayer(AnimatedLayer):
    """
    Layer that scrolls from left to right across the screen.
    """
    def __init__(self, image_layer, padding=0):
        
        AnimatedLayer.__init__(self, image_layer)
        
        self.padding = np.zeros((8, padding, 3), dtype=np.uint8)
        
        
        
    def get_frame(self, frame_num):
        """
        Returns the frame frame_num of the layer. Frame 0 is the starting frame.
        """
        
        frame = self.image_layer.get_frame(frame_num)
        
        rgb   = np.concatenate((frame.rgb,   self.padding), axis=1)
        alpha = np.concatenate((frame.alpha, self.padding), axis=1)
        
        rgb   = np.roll(rgb,   frame_num, 1)
        alpha = np.roll(alpha, frame_num, 1)
        
        return Frame(rgb[:,:8,:], alpha[:,:8,0])
        


class FlashingLayer(AnimatedLayer):
    """
    Layer that can flash on and off. The input flash_sequence should be a list
    of values between 0 and 255. The flash sequence will display the full image
    for frame i when flash_sequence[i] is equal to 255, and will display no
    image when flash_sequence[i] equals 0. values in between 0 and 255 are also
    allowed, and the image will be partially visible depending on the chosen
    value. The sequence will be repeated if an index greater than
    len(flash_sequence) is chosen.
    """
    
    def __init__(self, image_layer, flash_sequence=[255,0]):
                     
        AnimatedLayer.__init__(self, image_layer)
                 
        self.flash_sequence = flash_sequence
        
    
    def get_frame(self, frame_num=1):
        """
        Returns the frame frame_num of the layer. Frame 0 is the starting frame.
        """
        
        frame = self.image_layer.get_frame(frame_num)
        
        # Get the intensity of the rgb image
        flash_idx = frame_num % len(self.flash_sequence)
        intensity = self.flash_sequence[flash_idx]     
        
        alpha = np.uint8( frame.alpha * (intensity/255) )
        
        return Frame(frame.rgb, alpha[:,:,1])
        
        
