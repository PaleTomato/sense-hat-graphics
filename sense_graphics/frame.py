import numpy as np

class Frame(object):
    """
    Image frame for displaying on the Sense Hat.
    
    Each frame comprises of an rgb array (8x8x3) which defines the rgb values
    of each one of the 64 pixels, and an alpha array (8x8) which defines the
    transparency of each pixel in the frame. Frames can be added together,
    which returns a new frame with the images combined together. Areas that are
    transparent (i.e. with alpha < 255) on the first frame, will allow elements
    of the second frame to show through. In this way it is possible to draw a
    complex image by combining a number of simpler images.
    
    Methods:
    --------
    to_list   - Return the red, green and blue values as a 64 element list.
    __add__   - Overridden add method to add 2 frames together.
    __radd__  - Overridden add method to add 2 frames together.
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
        Overridden add method that can sum two Frame objects.
        
        Adding two frames will produce a new frame as an output with the two
        images combined. The first image in the sum will be displayed in front
        of the second.
        """
        if other.__class__ != Frame:
            raise TypeError
        
        # Calculate the alpha for both frames
        alpha1 = self.alpha
        alpha2 = np.uint8( other.alpha * ((255 - self.alpha) / 255) )
        alpha_total = alpha1 + alpha2
        
        # identify non-zero alpha values (to prevent division by zero later)
        alpha_nz = alpha_total != 0
        
        # Calculate rgb of both frames
        rgb_total = np.zeros((8, 8, 3), dtype=np.uint8)
        rgb_total[alpha_nz] += (
            self.rgb[alpha_nz]  * (alpha1[alpha_nz] / alpha_total[alpha_nz]) )
        rgb_total[alpha_nz] += (
            other.rgb[alpha_nz] * (alpha2[alpha_nz] / alpha_total[alpha_nz]) )
        
        
        return Frame(rgb_total, alpha_total[:,:,1])
        
    
    def __radd__(self, other):
        """
        Overridden right add method that uses new add method.
        """
        
        if other == 0:
            return self
        else:
            return self.__add__(other)
            
    
    def to_list(self, use_alpha=True):
        """
        Return the red, green and blue values as a 64 element list.
        
        Convert the Frame's rgb values from a numpy array to a list that is
        compatible with the Sense Hat's set_pixels method. Each list item
        contains a 3 element list of rgb integer values between 0 and 255.
        
        Inputs:
        -------
        use_alpha - Set to True to multiply the rgb values by the stored alpha
                    values before returning the list. Set to False to return
                    rgb values with no additional multiplying.
        """
        
        if use_alpha:
            values  = np.uint8(self.rgb  * (self.alpha/255))
            
        else:
            values  = self.rgb
            
        values = values.reshape(64,3)
        
        return values.tolist()
            
