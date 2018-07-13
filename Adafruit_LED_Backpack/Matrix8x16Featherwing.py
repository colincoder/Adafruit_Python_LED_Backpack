# Copyright (c) 2017 Adafruit Industries
# Author: Carter Nelson
# Modified from Matrix8x8 by Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from . import HT16K33
from PIL import Image
from PIL import ImageDraw
import time

class Matrix8x16(HT16K33.HT16K33):
    """Single color 8x16 matrix LED backpack display."""

    def __init__(self, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        super(Matrix8x16, self).__init__(**kwargs)

# 8x8 monochrome bitmap fonts for rendering
# Author: Daniel Hepper <daniel@hepper.net>
# 
# License: Public Domain
# 
# Based on:
#  Summary: font8x8.h
#  8x8 monochrome bitmap fonts for rendering
# 
#  Author:
#      Marcel Sondaar
#      International Business Machines (public domain VGA fonts)
# 
#  License:
#      Public Domain

    font8x8 = {
        ' ':    [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],   
        '!':    [ 0x18, 0x3C, 0x3C, 0x18, 0x18, 0x00, 0x18, 0x00],   
        '"':    [ 0x36, 0x36, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],   
        '#':    [ 0x36, 0x36, 0x7F, 0x36, 0x7F, 0x36, 0x36, 0x00],   
        '$':    [ 0x0C, 0x3E, 0x03, 0x1E, 0x30, 0x1F, 0x0C, 0x00],   
        '%':    [ 0x00, 0x63, 0x33, 0x18, 0x0C, 0x66, 0x63, 0x00],   
        '&':    [ 0x1C, 0x36, 0x1C, 0x6E, 0x3B, 0x33, 0x6E, 0x00],   
        '\'':   [ 0x06, 0x06, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00],   
        '(':    [ 0x18, 0x0C, 0x06, 0x06, 0x06, 0x0C, 0x18, 0x00],   
        ')':    [ 0x06, 0x0C, 0x18, 0x18, 0x18, 0x0C, 0x06, 0x00],   
        '*':    [ 0x00, 0x66, 0x3C, 0xFF, 0x3C, 0x66, 0x00, 0x00],   
        '+':    [ 0x00, 0x0C, 0x0C, 0x3F, 0x0C, 0x0C, 0x00, 0x00],   
        ',':    [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C, 0x06],   
        '-':    [ 0x00, 0x00, 0x00, 0x3F, 0x00, 0x00, 0x00, 0x00],   
        '.':    [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C, 0x00],   
        '/':    [ 0x60, 0x30, 0x18, 0x0C, 0x06, 0x03, 0x01, 0x00],  
# Made Zero narrower
#        '0':    [ 0x3E, 0x63, 0x73, 0x7B, 0x6F, 0x67, 0x3E, 0x00],   
        '0':    [ 0x1E, 0x33, 0x33, 0x33, 0x33, 0x33, 0x1E, 0x00],   
        '1':    [ 0x0C, 0x0E, 0x0C, 0x0C, 0x0C, 0x0C, 0x3F, 0x00],   
        '2':    [ 0x1E, 0x33, 0x30, 0x1C, 0x06, 0x33, 0x3F, 0x00],   
        '3':    [ 0x1E, 0x33, 0x30, 0x1C, 0x30, 0x33, 0x1E, 0x00], 
# MAde four narrower
#        '4':    [ 0x38, 0x3C, 0x36, 0x33, 0x7F, 0x30, 0x78, 0x00],   
        '4':    [ 0x18, 0x1C, 0x1E, 0x1B, 0x3F, 0x18, 0x3C, 0x00],   
        '5':    [ 0x3F, 0x03, 0x1F, 0x30, 0x30, 0x33, 0x1E, 0x00],   
        '6':    [ 0x1C, 0x06, 0x03, 0x1F, 0x33, 0x33, 0x1E, 0x00],   
        '7':    [ 0x3F, 0x33, 0x30, 0x18, 0x0C, 0x0C, 0x0C, 0x00],   
        '8':    [ 0x1E, 0x33, 0x33, 0x1E, 0x33, 0x33, 0x1E, 0x00],   
        '9':    [ 0x1E, 0x33, 0x33, 0x3E, 0x30, 0x18, 0x0E, 0x00],   
        ':':    [ 0x00, 0x0C, 0x0C, 0x00, 0x00, 0x0C, 0x0C, 0x00],   
        ';':    [ 0x00, 0x0C, 0x0C, 0x00, 0x00, 0x0C, 0x0C, 0x06],   
        '<':    [ 0x18, 0x0C, 0x06, 0x03, 0x06, 0x0C, 0x18, 0x00],   
        '=':    [ 0x00, 0x00, 0x3F, 0x00, 0x00, 0x3F, 0x00, 0x00],   
        '>':    [ 0x06, 0x0C, 0x18, 0x30, 0x18, 0x0C, 0x06, 0x00],   
        '?':    [ 0x1E, 0x33, 0x30, 0x18, 0x0C, 0x00, 0x0C, 0x00],   
        '@':    [ 0x3E, 0x63, 0x7B, 0x7B, 0x7B, 0x03, 0x1E, 0x00],   
        'A':    [ 0x0C, 0x1E, 0x33, 0x33, 0x3F, 0x33, 0x33, 0x00],   
        'B':    [ 0x3F, 0x66, 0x66, 0x3E, 0x66, 0x66, 0x3F, 0x00],   
        'C':    [ 0x3C, 0x66, 0x03, 0x03, 0x03, 0x66, 0x3C, 0x00],   
        'D':    [ 0x1F, 0x36, 0x66, 0x66, 0x66, 0x36, 0x1F, 0x00],   
        'E':    [ 0x7F, 0x46, 0x16, 0x1E, 0x16, 0x46, 0x7F, 0x00],   
        'F':    [ 0x7F, 0x46, 0x16, 0x1E, 0x16, 0x06, 0x0F, 0x00],   
        'G':    [ 0x3C, 0x66, 0x03, 0x03, 0x73, 0x66, 0x7C, 0x00],   
        'H':    [ 0x33, 0x33, 0x33, 0x3F, 0x33, 0x33, 0x33, 0x00],   
        'I':    [ 0x1E, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x1E, 0x00],   
        'J':    [ 0x78, 0x30, 0x30, 0x30, 0x33, 0x33, 0x1E, 0x00],   
        'K':    [ 0x67, 0x66, 0x36, 0x1E, 0x36, 0x66, 0x67, 0x00],   
        'L':    [ 0x0F, 0x06, 0x06, 0x06, 0x46, 0x66, 0x7F, 0x00],   
        'M':    [ 0x63, 0x77, 0x7F, 0x7F, 0x6B, 0x63, 0x63, 0x00],   
        'N':    [ 0x63, 0x67, 0x6F, 0x7B, 0x73, 0x63, 0x63, 0x00],   
        'O':    [ 0x1C, 0x36, 0x63, 0x63, 0x63, 0x36, 0x1C, 0x00],   
        'P':    [ 0x3F, 0x66, 0x66, 0x3E, 0x06, 0x06, 0x0F, 0x00],   
        'Q':    [ 0x1E, 0x33, 0x33, 0x33, 0x3B, 0x1E, 0x38, 0x00],   
        'R':    [ 0x3F, 0x66, 0x66, 0x3E, 0x36, 0x66, 0x67, 0x00],   
        'S':    [ 0x1E, 0x33, 0x07, 0x0E, 0x38, 0x33, 0x1E, 0x00],   
        'T':    [ 0x3F, 0x2D, 0x0C, 0x0C, 0x0C, 0x0C, 0x1E, 0x00],   
        'U':    [ 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x3F, 0x00],   
        'V':    [ 0x33, 0x33, 0x33, 0x33, 0x33, 0x1E, 0x0C, 0x00],   
        'W':    [ 0x63, 0x63, 0x63, 0x6B, 0x7F, 0x77, 0x63, 0x00],   
        'X':    [ 0x63, 0x63, 0x36, 0x1C, 0x1C, 0x36, 0x63, 0x00],   
        'Y':    [ 0x33, 0x33, 0x33, 0x1E, 0x0C, 0x0C, 0x1E, 0x00],   
        'Z':    [ 0x7F, 0x63, 0x31, 0x18, 0x4C, 0x66, 0x7F, 0x00],   
        '[':    [ 0x1E, 0x06, 0x06, 0x06, 0x06, 0x06, 0x1E, 0x00],   
        '\\':   [ 0x03, 0x06, 0x0C, 0x18, 0x30, 0x60, 0x40, 0x00],   
        ']':    [ 0x1E, 0x18, 0x18, 0x18, 0x18, 0x18, 0x1E, 0x00],   
        '^':    [ 0x08, 0x1C, 0x36, 0x63, 0x00, 0x00, 0x00, 0x00],   
        '_':    [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF],   
        '`':    [ 0x0C, 0x0C, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00],   
        'a':    [ 0x00, 0x00, 0x1E, 0x30, 0x3E, 0x33, 0x6E, 0x00],   
        'b':    [ 0x07, 0x06, 0x06, 0x3E, 0x66, 0x66, 0x3B, 0x00],   
        'c':    [ 0x00, 0x00, 0x1E, 0x33, 0x03, 0x33, 0x1E, 0x00],   
        'd':    [ 0x38, 0x30, 0x30, 0x3e, 0x33, 0x33, 0x6E, 0x00],   
        'e':    [ 0x00, 0x00, 0x1E, 0x33, 0x3f, 0x03, 0x1E, 0x00],   
        'f':    [ 0x1C, 0x36, 0x06, 0x0f, 0x06, 0x06, 0x0F, 0x00],   
        'g':    [ 0x00, 0x00, 0x6E, 0x33, 0x33, 0x3E, 0x30, 0x1F],   
        'h':    [ 0x07, 0x06, 0x36, 0x6E, 0x66, 0x66, 0x67, 0x00],   
        'i':    [ 0x0C, 0x00, 0x0E, 0x0C, 0x0C, 0x0C, 0x1E, 0x00],   
        'j':    [ 0x30, 0x00, 0x30, 0x30, 0x30, 0x33, 0x33, 0x1E],   
        'k':    [ 0x07, 0x06, 0x66, 0x36, 0x1E, 0x36, 0x67, 0x00],   
        'l':    [ 0x0E, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x1E, 0x00],   
        'm':    [ 0x00, 0x00, 0x33, 0x7F, 0x7F, 0x6B, 0x63, 0x00],   
        'n':    [ 0x00, 0x00, 0x1F, 0x33, 0x33, 0x33, 0x33, 0x00],   
        'o':    [ 0x00, 0x00, 0x1E, 0x33, 0x33, 0x33, 0x1E, 0x00],   
        'p':    [ 0x00, 0x00, 0x3B, 0x66, 0x66, 0x3E, 0x06, 0x0F],   
        'q':    [ 0x00, 0x00, 0x6E, 0x33, 0x33, 0x3E, 0x30, 0x78],   
        'r':    [ 0x00, 0x00, 0x3B, 0x6E, 0x66, 0x06, 0x0F, 0x00],   
        's':    [ 0x00, 0x00, 0x3E, 0x03, 0x1E, 0x30, 0x1F, 0x00],   
        't':    [ 0x08, 0x0C, 0x3E, 0x0C, 0x0C, 0x2C, 0x18, 0x00],   
        'u':    [ 0x00, 0x00, 0x33, 0x33, 0x33, 0x33, 0x6E, 0x00],   
        'v':    [ 0x00, 0x00, 0x33, 0x33, 0x33, 0x1E, 0x0C, 0x00],   
        'w':    [ 0x00, 0x00, 0x63, 0x6B, 0x7F, 0x7F, 0x36, 0x00],   
        'x':    [ 0x00, 0x00, 0x63, 0x36, 0x1C, 0x36, 0x63, 0x00],   
        'y':    [ 0x00, 0x00, 0x33, 0x33, 0x33, 0x3E, 0x30, 0x1F],   
        'z':    [ 0x00, 0x00, 0x3F, 0x19, 0x0C, 0x26, 0x3F, 0x00],   
        '{':    [ 0x38, 0x0C, 0x0C, 0x07, 0x0C, 0x0C, 0x38, 0x00],   
        '|':    [ 0x18, 0x18, 0x18, 0x00, 0x18, 0x18, 0x18, 0x00],   
        '}':    [ 0x07, 0x0C, 0x0C, 0x38, 0x0C, 0x0C, 0x07, 0x00],   
        '~':    [ 0x6E, 0x3B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   
        }



    def getcharimage(self,v):
        image = Image.new('1', (8, 8))   
        if ord(v) < 32 or ord(v) > 126:
            return image
        draw = ImageDraw.Draw(image)
        ch = self.font8x8[v]
        for x in range(0,8):
            for y in range(0,8):
                set = ch[x] & 1 << y
                pt = 1 if set else 0
                draw.point((7-x,y), pt)
        return image

    def setnumber(self,n,image):
        if n < 0 or n > 99:
            leftimage = self.getcharimage('-')
            rightimage = self.getcharimage('-')
        else:
            if n/10 == 0:
                leftdigit = ord(' ')
            else:
                leftdigit = ord('0') + n / 10
            rightdigit = ord('0') + n % 10
            leftimage = self.getcharimage(chr(leftdigit))
            rightimage = self.getcharimage(chr(rightdigit))
        image.paste(leftimage, (0, 0, 8, 8))
        image.paste(rightimage, (0, 7, 8, 15))



    def set_pixel(self, x, y, value):
        """Set pixel at position x, y to the given value.  X and Y should be values
        of 0 to 7 and 0 to 15, resp.  Value should be 0 for off and non-zero for on.
        """
        if x < 0 or x > 7 or y < 0 or y > 15:
            # Ignore out of bounds pixels.
            return
#CJS For the Adafruit 0.8" 8x16 LED Matrix FeatherWing the 2 displays have coordinates rotated by 90Deg
#    This corrects that.
        if y < 8:
            self.set_led( y * 16 + x, value)
        else:
            self.set_led((y-8) * 16 + (x+8), value)

    def get_pixel(self, x, y):
        """Get pixel at position x, y.  X and Y should be values
        of 0 to 7 and 0 to 15, resp.  Value are 0 for off and non-zero for on.
        """
        if x < 0 or x > 7 or y < 0 or y > 15:
            # Ignore out of bounds pixels.
            return
#CJS For the Adafruit 0.8" 8x16 LED Matrix FeatherWing the 2 displays have coordinates rotated by 90Deg
#    This corrects that.
        if y < 8:
            return self.get_led( y * 16 + x)
        else:
            return self.get_led((y-8) * 16 + (x+8))

    def set_image(self, image):
        """Set display buffer to Python Image Library image.  Image will be converted
        to 1 bit color and non-zero color values will light the LEDs.
        """
        imwidth, imheight = image.size
        if imwidth != 8 or imheight != 16:
            raise ValueError('Image must be an 8x16 pixels in size.')
        # Convert image to 1 bit color and grab all the pixels.
        pix = image.convert('1').load()
        # Loop through each pixel and write the display buffer pixel.
        for x in xrange(8):
            for y in xrange(16):
                color = pix[(x, y)]
                # Handle the color of the pixel, off or on.
                if color == 0:
                    self.set_pixel(x, y, 0)
                else:
                    self.set_pixel(x, y, 1)

    def get_image(self):
        """Set display buffer from hardware.
        """
        image = Image.new('1', (8, 16))
        draw = ImageDraw.Draw(image)
        for x in xrange(8):
            for y in xrange(16):
                draw.point((x,y),self.get_pixel(x, y))
        return image

    def create_blank_image(self):
        return Image.new("RGB", (8, 16))


    def vertical_scroll(self, image, padding=True):
        """Returns a list of images which appear to scroll from left to right
        across the input image when displayed on the LED matrix in order.

        The input image is not limited to being 8x16. If the input image is
        larger than this, then all columns will be scrolled through but only
        the top 16 rows of pixels will be displayed.

        Keyword arguments:
        image -- The image to scroll across.
        padding -- If True, the animation will begin with a blank screen and the
            input image will scroll into the blank screen one pixel column at a
            time. Similarly, after scrolling across the whole input image, the
            end of the image will scroll out of a blank screen one column at a
            time. If this is not True, then only the input image will be scroll
            across without beginning or ending with "whitespace."
            (Default = True)
        """

        image_list = list()
        width = image.size[0]
        # Scroll into the blank image.
        if padding:
            for x in range(8):
                section = image.crop((0, 0, x, 16))
                display_section = self.create_blank_image()
                display_section.paste(section, (8 - x, 0, 8, 16))
                image_list.append(display_section)

        #Scroll across the input image.
        for x in range(8, width + 1):
            section = image.crop((x - 8, 0, x, 16))
            display_section = self.create_blank_image()
            display_section.paste(section, (0, 0, 8, 16))
            image_list.append(display_section)

        #Scroll out, leaving the blank image.
        if padding:
            for x in range(width - 7, width + 1):
                section = image.crop((x, 0, width, 16))
                display_section = self.create_blank_image()
                display_section.paste(section, (0, 0, 7 - (x - (width - 7)), 16))
                image_list.append(display_section)

        #Return the list of images created
        return image_list

    def horizontal_scroll(self, image, padding=True):
        """Returns a list of images which appear to scroll from top to bottom
        down the input image when displayed on the LED matrix in order.

        The input image is not limited to being 8x16. If the input image is
        largerthan this, then all rows will be scrolled through but only the
        left-most 8 columns of pixels will be displayed.

        Keyword arguments:
        image -- The image to scroll down.
        padding -- If True, the animation will begin with a blank screen and the
            input image will scroll into the blank screen one pixel row at a
            time. Similarly, after scrolling down the whole input image, the end
            of the image will scroll out of a blank screen one row at a time.
            If this is not True, then only the input image will be scroll down
            without beginning or ending with "whitespace." (Default = True)
        """

        image_list = list()
        height = image.size[1]

        # Scroll into the blank image.
        if padding:
            for y in range(1,17):
                section = image.crop((0, 0, 8, y))
                print section.width,section.height
                display_section = self.create_blank_image()
                display_section.paste(section, (0, 16 - y, 8, 16))
                image_list.append(display_section)
        return image_list

        #Scroll across the input image.
        for y in range(16, height + 1):
            section = image.crop((0, y - 16, 8, y))
            display_section = self.create_blank_image()
            display_section.paste(section, (0, 0, 8, 16))
            image_list.append(display_section)

        #Scroll out, leaving the blank image.
        if padding:
            for y in range(height - 15, height + 1):
                section = image.crop((0, y, 8, height))
                display_section = self.create_blank_image()
                display_section.paste(section, (0, 0, 8, 15 - (y - (height - 15))))
                image_list.append(display_section)

        #Return the list of images created
        return image_list

    def animate(self, images, delay=.25):
        """Displays each of the input images in order, pausing for "delay"
        seconds after each image.

        Keyword arguments:
        image -- An iterable collection of Image objects.
        delay -- How many seconds to wait after displaying an image before
            displaying the next one. (Default = .25)
        """
        for image in images:
            # Draw the image on the display buffer.
            self.set_image(image)

            # Draw the buffer to the display hardware.
            self.write_display()
            time.sleep(delay)

    def setsprite(self, x, y, image, char):  # display a character at the indicated position on the screen
        image.paste(char, (x,y))             # the coords can be off the screen
        self.set_image(image)
        self.write_display()


    def print_str(self,image,text,repeat=1,speed=0.01):
        length = len(text)  # get the character count
        if length < 1:
            return
        for loop in range(repeat):
            for y in range(0,(length*8) + 16):  # the step count is width of the characters plus the display with
                for x in range(length):         # maybe move a character
                    pos = 16 + (x * 8) - y      # where will it start
                    if pos < 16 and pos > -8:   # only display if it's on the screen
                        self.setsprite(0,pos,image,self.getcharimage(text[x]))
                time.sleep(speed)
