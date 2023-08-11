"""
MIT License

Copyright (c) 2023 tofh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#---------------------------------------------#

# Author: tofh
# Last Updated: 10-08-2023
# Description: utilities used by xonotic-chat-server...

#---------------------------------------------#
import libcolors, random


#------------------------------#
# text color encoding
#------------------------------#

## HSL ENCODE
def encode_hsl(text, h=0, s=100, l=50):
    """
    Encode input text using hsl colorspace
    """
    colored_text = ""
    if 360 / len(text) < 0.6:
        inc_h = 1
    else:
        inc_h = round(360/len(text))

    for i in range(len(text)):
        current_char = text[i]
        if current_char.isspace():
            colored_text += current_char
        else:
            if h > 360:
                h = 0
            colored_text += libcolors.rgb2xon(libcolors.hsl2rgb(h, s, l)) + current_char
            h += inc_h
    return colored_text + "^7"

## RGB ENCODE
def encode_rgb(text, start, stop):
    """
    Encode input text using rgb colorspace
    """
    colored_text = ""
    for i in range(len(text)):
        current_char = text[i]
        if current_char.isspace():
            colored_text += current_char
        else:
            colored_text += libcolors.rgb2xon(libcolors.color_lerp(start, stop, i / len(text))) + current_char
    return colored_text + "^7"


# rainbow
def rainbow_encode(text):
    """
    add rainbow colors
    """
    return encode_hsl(text)

def rand_rainbow_encode(text):
    """
    Add random rainbow colors, using a random starting point
    """
    h = random.randint(0, 361)
    return encode_hsl(text, h=h)


# Colors
def color_encode(text, start, stop):
    """
    add color gradient, takes xonotic color code value without the carat
    """
    return encode_rgb(text, libcolors.xon2rgb(start), libcolors.xon2rgb(stop))


def rand_color_encode(text):
    """
    add random color gradient, using random start stop values
    """
    start = libcolors.hsl2rgb(random.randint(0, 361), 100, 50)
    stop = libcolors.hsl2rgb(random.randint(0, 361), 100, 50)
    return encode_rgb(text, start, stop)


#-------------------------#
#   Misc
#-------------------------#

def help():
    """
    Convert help.txt to xonotic console output
    and send it...
    """
    message = "echo;"
    guide = open("help.txt", "r")
    for line in guide.readlines():
        message += f'echo "{line.rstrip()}";'
    guide.close()
    return message + "echo"

def validColorCode(color_code):
    """
    Checks if the xon color code is valid, boolen result
    """
    if len(color_code) == 3:
        try:
            if int(color_code, 16) <= 4095:
                return True
        except:
            return False
    else:
        return False

