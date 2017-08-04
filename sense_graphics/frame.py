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
            
        
        self.rgb = image_rgb
        self.alpha = image_alpha
        
    def __add__(self, other):
        
        if other.__class__ != Frame:
            raise TypeError
        
        this_alpha  = self.alpha
        other_alpha = (other.alpha * (255-self.alpha))//255
        
        # Multiply rgb by alpha (by making alpha into 8x8x3)
        this_rgb  = self.rgb  * np.repeat( this_alpha[:,:,np.newaxis],3,axis=2)
        other_rgb = other.rgb * np.repeat(other_alpha[:,:,np.newaxis],3,axis=2)
        
        new_rgb   = (this_rgb + other_rgb)//255
        new_alpha = this_alpha + other_alpha
        
        return Frame(new_rgb, new_alpha)
        
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
            
