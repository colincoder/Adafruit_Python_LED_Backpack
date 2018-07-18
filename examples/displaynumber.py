# Copyright (c) 2018 Colin Stearman
# Author: Colin Stearman
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

# display a number
# python displaynumber.py {n}
#  0 <= n <= 99
#  n outside that range displays --

import sys
import time

from PIL import Image
from PIL import ImageDraw

from Adafruit_LED_Backpack import FeatherMatrix8x16

# Create display instance on default I2C address (0x70) and bus number.
display = FeatherMatrix8x16.FeatherMatrix8x16()

# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x16.Matrix8x16(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
display.begin()
image = Image.new('1', (8, 16))
draw = ImageDraw.Draw(image)

v = int(sys.argv[1])
display.setnumber(v,image)
#draw.rectangle((6,14,7,15), outline=255, fill=0)
display.set_image(image)
display.write_display()
print "Number Displayed"
sys.exit(0)
