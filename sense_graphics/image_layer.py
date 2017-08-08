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
        
        self.name   = name
        
    
    def get_frame(self, frame_num=1):
        """
        Returns the frame frame_num of the layer. For a static layer this will
        always be the same as the main image layer. Frame 0 is the starting
        frame.
        """
        
        return Frame(self.rgb,self.alpha)
        
    
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


class StaticLayer(ImageLayer):
    """
    Static image layer that stays in the same place on the screen.
    """
    def __init__(self, rgb, alpha, name="Static Layer 1"):
        
        ImageLayer.__init__(self, rgb, alpha, name)
    
    
class ScrollingLayer(ImageLayer):
    """
    Layer that scrolls from left to right across the screen.
    """
    def __init__(self, rgb, alpha, name="Moving Layer 1", padding=0):
        
        ImageLayer.__init__(self, rgb, alpha, name)
        
        if padding > 0:
            rgb_pad = np.zeros((8, padding, 3), dtype=np.uint8)
            alpha_pad = np.zeros((8, padding),  dtype=np.uint8)
            
            self.rgb   = np.concatenate((self.rgb,   rgb_pad  ), axis=1)
            self.alpha = np.concatenate((self.alpha, alpha_pad), axis=1)
        
        
        
        
    def get_frame(self, frame_num):
        """
        Returns the frame frame_num of the layer. Frame 0 is the starting frame.
        """
        
        rgb   = np.roll(self.rgb,   frame_num, 1)
        alpha = np.roll(self.alpha, frame_num, 1)
        
        return Frame(rgb[:,:8,:], alpha[:,:8])
        


class FlashingLayer(ImageLayer):
    """
    Layer that can flash on and off. The input flash_sequence should be a list
    of values between 0 and 255. The flash sequence will display the full image
    for frame i when flash_sequence[i] is equal to 255, and will display no
    image when flash_sequence[i] equals 0. values in between 0 and 255 are also
    allowed, and the image will be partially visible depending on the chosen
    value. The sequence will be repeated if an index greater than
    len(flash_sequence) is chosen.
    """
    
    def __init__(self,
                 rgb,
                 alpha,
                 name="Flashing Layer 1",
                 flash_sequence=[255,0]
                 ):
                 
        ImageLayer.__init__(self, rgb, alpha, name)
        
        self.flash_sequence = flash_sequence
        
    
    def get_frame(self, frame_num=1):
        """
        Returns the frame frame_num of the layer. Frame 0 is the starting frame.
        """
        
        # Get the intensity of the rgb image
        flash_idx = frame_num % len(self.flash_sequence)
        intensity = self.flash_sequence[flash_idx]     
        
        alpha = np.uint8( self.alpha * (intensity/255) )
        
        return Frame(self.rgb, alpha)
        
        
