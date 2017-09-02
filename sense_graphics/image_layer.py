from __future__ import absolute_import
import numpy as np
from .frame import Frame

class ImageLayer(object):
    """
    Base image layer class.
    
    The ImageLayer class is a base class which is used for creating a new layer
    of imagery to display on the Sense Hat LED matrix. It contains the red,
    green and blue (rgb) values as well as the alpha values.
    """
    
    def __init__(self, rgb, alpha, name="Layer 1"):
        """
        Initialise the Image Layer with rgb and alpha values, and a name.
        
        Inputs:
        -------
        rgb   - The red, green and blue values of the image, as a 64 element
                list, each element of which contains a 3 element list of
                integer rgb values from 0 to 255.
        alpha - The alpha values of the second image, as a 64 element list of
                values from 0 to 255.
        name  - The name of this image layer, as a string.
        """
        
        
        # Convert rgb and alpha to numpy arrays
        rgb   = np.array(rgb, dtype = np.uint8)
        alpha = np.array(alpha, dtype = np.uint8)
        
        # Reshape from 64x3 to 8x8x3
        self.rgb   = rgb.reshape(8,8,3)
        self.alpha = alpha.reshape(8,8)
        
        self.num_frames = 1

        self.name  = name
    
    
    def __getitem__(self, idx):
        """
        Return the frame at index idx.
        
        Overrides the built-in __getitem__ method to instead return the frame
        at the inputted index. If idx is greater than the length defined by
        len(self) then the frames will loop around and the appropriate frame
        will be returned instead.
        """
        
        # TODO make sure input is integer
        
        if idx >= len(self) or idx < 0:
            frame_num = idx % len(self)
        
        else:
            frame_num = idx
        
        rgb, alpha = self.get_pixels(frame_num)
        
        return Frame(rgb, alpha)
    
    
    def __repr__(self):
        
        return self.__class__.__name__ + '("' + self.name + '")'
    
    
    def get_pixels(self, frame_num=0):
        """
        Returns the rgb and alpha values for frame frame_num of the layer.
        """
        
        return (self.rgb, self.alpha)
        
        
    def get_name(self):
        
        return self.name
        
    
    def __len__(self):
        """
        Return the number of frames for this object.
        
        Overrides the built-in __len__method to instead return the number of
        frames in this layer
        """
        
        return self.num_frames


class AnimatedLayer(ImageLayer):
    """
    Class for an animated layer. All animated layers should be subclassed off
    this class.
    """
    
    def __init__(self, image_layer):
        
        self.image_layer = image_layer
    
    
    def get_pixels(self, frame_num=0):
        
        return self.image_layer.get_pixels()
        
        
    def get_name(self):
        
        return self.image_layer.get_name()
    
    
    def __repr__(self):
        
        inner_brackets = self.image_layer.__repr__()
        return self.__class__.__name__ + '(' + inner_brackets + ')'
        

class ScrollingLayer(AnimatedLayer):
    """
    Layer that scrolls from left to right across the screen.
    """
    
    def __init__(self, image_layer, direction='E', padding=0):
        """
        Initialise the ScrollingLayer with direction and padding.
        
        Inputs:
        -------
        image_layer   - The layer to apply the effect to. This can be either
                        an ImageLayer object, or a subclass of it.
        direction     - The direction in which to scroll. Use 'N', 'S', 'E' or
                        'W' to scroll north (up) south (down) east (left) or
                        west (right) respectively.
        padding       - The number of blank pixels to append to the image when 
                        scrolling. A padding of 8 would mean that your image
                        will scroll entirely off the display before it
                        reappears on the other side.
        """
        
        AnimatedLayer.__init__(self, image_layer)
        
        if direction in ('N','S'):
            self.padding = np.zeros((padding, 8, 3), dtype=np.uint8)
            self.axis = 0
            
        elif direction in ('E','W'):
            self.padding = np.zeros((8, padding, 3), dtype=np.uint8)
            self.axis = 1
            
        
        if direction in ('S','E'):
            self.shift_dir = 1
            
        elif direction in ('N','W'):
            self.shift_dir = -1
            
        
        self.num_frames = 8 + padding
        
        
    def get_pixels(self, frame_num=0):
        """
        Returns the rgb and alpha values for frame frame_num of the layer.
        """
        
        rgb, alpha = self.image_layer.get_pixels(frame_num)
        
        rgb   = np.concatenate((rgb,   self.padding), axis=self.axis)
        alpha = np.concatenate((alpha, self.padding[:,:,1]), axis=self.axis)
        
        shift = self.shift_dir * frame_num
        rgb   = np.roll(rgb,   shift, self.axis)
        alpha = np.roll(alpha, shift, self.axis)
        
        return (rgb[:8,:8,:], alpha[:8,:8])
        


class FlashingLayer(AnimatedLayer):
    """
    Layer that can flash on and off in a specified sequence.
    """
    
    def __init__(self, image_layer, pattern=[255,0]):
        """
        Initialise the ScrollingLayer with direction and padding.
        
        Inputs:
        -------
        image_layer   - The layer to apply the effect to. This can be either
                        an ImageLayer object, or a subclass of it.
        pattern       - List of integer values from 0 to 255. In a similar way
                        to an image layer's alpha values, a value of 0 will
                        make the image completely invisible, and a value of 255
                        opaque. By setting values in between these extremes you
                        can make an image fade over a series of frames.
        """
        
        AnimatedLayer.__init__(self, image_layer)
                 
        self.pattern = pattern
        self.num_frames     = len(pattern)
        
    
    def get_pixels(self, frame_num=0):
        """
        Returns the rgb and alpha values for frame frame_num of the layer.
        """
        
        rgb, alpha = self.image_layer.get_pixels(frame_num)
        
        # Get the intensity of the rgb image
        flash_idx = frame_num % len(self.pattern)
        intensity = self.pattern[flash_idx]     
        
        alpha = np.uint8( alpha * (intensity/255) )
        
        return (rgb, alpha)
        