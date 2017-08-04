from __future__ import absolute_import
import numpy as np
from .frame import Frame

class ImageLayer(object):
    def __init__(self, rgb, alpha, name="Layer 1"):
        
        # Convert rgb and alpha to numpy arrays
        rgb   = np.array(rgb)
        alpha = np.array(alpha)
        
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
    def __init__(self, rgb, alpha, name="Moving Layer 1"):
        
        ImageLayer.__init__(self, rgb, alpha, name)
        
        
    def get_frame(self, frame_num=1):
        """
        Returns the frame frame_num of the layer. Frame 0 is the starting frame.
        """
        
        rgb   = np.roll(self.rgb,   frame_num, 1)
        alpha = np.roll(self.alpha, frame_num, 1)
        
        return Frame(rgb, alpha)
        
