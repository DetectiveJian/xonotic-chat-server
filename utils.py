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
# Last Updated: 07-08-2023
# Description: utilities used by xonotic-chat-server...

#---------------------------------------------#
import libcolors, random


#------------------------------#
# text color encoding
#------------------------------#


def color(text, option="random", extra=None):
    """
    add xonotic color code to the input text,
    option:
        color  - gradient colors
        random - adds random colors
        rainbow - adds rainbow colors
    """

    colored_text =  ""
    l = len(text)
    if 360/l < 0.6:
        inc = 1
    else:
        inc = 360/l
    # normalize the t function
    f = lambda t: t/l

    # Randomly color the input text
    if option == "random":
        # get a random value
        start = random.randint(0, 361)
        for i in range(l):
            current_char = text[i]
            if start > 360:
                start = 0

            if current_char.isspace():
                colored_text += current_char
            else:
                colored_text += libcolors.rgb2xon(libcolors.hsl2rgb(start, 100, 50)) + current_char
                start += inc
        return colored_text + "^7"

    # Rainbow color
    elif option == "rainbow":
        start = 0
        for i in range(l):
            current_char = text[i]
            if start > 360:
                start = 0
            if current_char.isspace():
                colored_text += current_char
            else:
                colored_text += libcolors.rgb2xon(libcolors.hsl2rgb(start, 100, 50)) + current_char
                start += inc
        return colored_text + "^7"

    # if color option, then use the colors provided, to encode the colors accordingly
    elif option == "color":
        start = libcolors.xon2rgb(extra[0])
        stop = libcolors.xon2rgb(extra[1])

        for i in range(l):
            current_char = text[i]
            if current_char.isspace():
                colored_text += current_char
            else:
                colored_text += libcolors.rgb2xon(libcolors.color_lerp(start, stop, f(i))) + current_char
        return colored_text + "^7"


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
        message += f'echo "{line.strip()}";'
    guide.close()
    return message + "echo"

