import numpy as np

class Frame(object):
    """
    Image frame for displaying on the Sense Hat. Each frame comprises of an rgb
    array (8x8x3) which defines the rgb values of each one of the 64 pixels, and
    an alpha array (8x8) which defines the transparency of each pixel in the
    frame. Frames can be added together, which returns a new frame with the
    images combined together. Areas that are transparent (i.e. with alpha < 255)
    on the first frame, will allow elements of the second frame to show through.
    In this way it is possible to draw a complex image by combining a number of
    simpler images. 
    """
    def __init__(self, image_rgb, image_alpha):
        
        # Check that inputs are numpy arrays
        if type(image_rgb)   != np.ndarray:
            raise TypeError("Input image_rgb should be a numpy array")
        
        if type(image_alpha) != np.ndarray:
            raise TypeError("Input image_alpha should be a numpy array")
        
        # Check size of inputted arrays are correct
        if image_rgb.shape != (8,8,3):
            raise ValueError("dimensions of image_rgb should be 8x8x3")
        
        if image_alpha.shape != (8,8):
            raise ValueError("dimensions of image_alpha should be 8x8")
            
        
        self.rgb   = image_rgb
        
        # Resize alpha into 8x8x3 (same size as rgb)
        self.alpha = np.repeat( image_alpha[:,:,np.newaxis],3,axis=2)
        
    def __add__(self, other):
        """
        Adding two frames will produce a new frame as an output with the two
        images combined. The first image in the sum will be displayed in front
        of the second
        """
        if other.__class__ != Frame:
            raise TypeError
        
        
        other_alpha = (other.alpha * (255-self.alpha))//255
        
        # Multiply rgb by alpha (by making alpha into 8x8x3)
        this_rgb  = self.rgb  * self.alpha
        other_rgb = other.rgb * other_alpha
        
        new_rgb   = (this_rgb + other_rgb)//255
        new_alpha = self.alpha + other_alpha
        
        return Frame(new_rgb, new_alpha[:,:,1])
        
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
            
    
    def to_list(self,use_alpha=False):
        """
        Converts the Frame rgb values from a numpy array to a list containing
        64 smaller lists of rgb values. This is useful for convering a frame
        in order to plot on the Sense hat.
        """
        
        if use_alpha:
            values  = (self.rgb  * self.alpha)//255
            
        else:
            values  = self.rgb
            
        values = values.reshape(64,3)
        
        return values.tolist()
            
