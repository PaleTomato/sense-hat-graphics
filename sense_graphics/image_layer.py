import numpy as np

class ImageLayer(object):
    def __init__(self, image, name="Layer 1"):
        self.image = image
        self.name  = name
        
    def get_frames(self):
        """
        Returns each unique frame of the layer.
        """
        return [self.image]


class StaticLayer(ImageLayer):
    def __init__(self, image, name="Static Layer 1"):
        ImageLayer.__init__(self, image, name)
    
class ScrollingLayer(ImageLayer):
    
    def __init__(self, image, name="Moving Layer 1", direction="L", padding=0):
        ImageLayer.__init__(self, image, name)
        self.direction = direction
        self.padding   = padding
        
    def get_frames(self):
        
        frames = []
        
        # Convert image to numpy array
        image = np.array(self.image)
        
        # Reshape from 64x3 to 8x8x3
        image = image.reshape(8,8,3)
        
        # TODO Add on the padding
        
        # Loop through generating each image
        for i in range(image.shape[1]):
            rolledimage = np.roll(image, i, 1)
            
            # Take only the 8x8 frame from the full image
            frame = rolledimage[:,0:8,:]
            
            # Add this frame to the list
            frame = frame.reshape(64,3)
            frames.append(frame.tolist())
            
        return frames
        
        
        
