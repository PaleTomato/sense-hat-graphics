# sense-hat-graphics
A Python module that extends the Raspberry Pi SenseHat class to display a
variety of graphics on the LED array.

## Classes
There are two classes that extend the
SenseHat class: the SenseImage and SenseGraph classes. Both primarily add new
ways of displaying on the LED matrix, but retain all the other functionality
privided by the SenseHat class.

### SenseImage
The SenseImage class is used for creating more complex images on the Sense Hat
LED matrix from a number of simpler images. The images are layered up one on
top of the other, and each can either be a static image or have animations
such as flashing or scrolling across the screen.

### SenseGraph
The SenseGraph is used to turn the LED matrix into a simple bar graph. This can
be used for a variety of purposes. Rather than plotting all the bars at once,
the bars are added one by one, shifting existing bars to the left. This
behaviour makes it useful for monitoring tasks, such as a CPU monitor, or else
tracking the humidity recorded by the Sense Hat.

## Usage
Naturally the usage varies between the two main classes, so see below for
whichever you are interested in.
