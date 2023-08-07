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

#--------------------------------------------------------#

# Author: tofh
# Last Updated: 07-08-2023
# Library containing color manipulation tools...

#--------------------------------------------------------#

#===================================#
# RGB Colorspace
#===================================#

def color_lerp(a, b, t):
    """
    Color Interpolation
    Takes two RGB tuples as input and time function
    Outputs a single RGB tuple
    """
    # c = a + (b - a) * t
    f = lambda a, b, t : int(a + ( b - a ) * t)

    r = f(a[0], b[0], t)
    g = f(a[1], b[1], t)
    b = f(a[2], b[2], t)

    return (r, g, b)


def rgb2xon(c):
    """
    Convert RGB colors to Xon equivalent color code
    Input: (r, g, b) Tuple
    """
    f = lambda x : hex(int((x / 255) * 15))

    r = f(c[0]).replace("0x", "")
    g = f(c[1]).replace("0x", "")
    b = f(c[2]).replace("0x", "")

    return "^x" + r + g + b


def xon2rgb(c):
    """
    Convert Xonotic color code to RBG values
    Input: string 0ff, ff0, etc
    """
    f = lambda x : int((int(str(x), 16) / 15) * 255)

    r = f(c[0])
    g = f(c[1])
    b = f(c[2])

    return (r, g, b)


def randrgb():
    """
    Generate random (r, g, b) tuple
    """
    f = lambda : random.randint(0, 256)

    return (f(), f(), f())


def css2rgb(c):
    """
    Convert CSS color code to rgb values
    takes 6 digit hex value without "#"
    returns a (r, g, b) tuple
    """
    f = lambda x : int(str(x), 16)

    r = f(c[0:2])
    g = f(c[2:4])
    b = f(c[4:])

    return (r, g, b)


def xonfilter(c):
    """
    Remove Xon color codes from input string.
    """
    text = ""
    pointer = 0

    # looping through the input string
    while True:
        # if pointer exceeds the length of the input string, exit the loop
        if pointer > len(c) -1:
            break
        # else, get a character from the input string using pointer as index
        else:
            current_char = c[pointer]
            # if current char is carat "^", look if it's the last entry of the input text
            # meaning if current char is carat and pointer is equal to the input string length 
            # add the current char to the text string and exit the loop
            if current_char == "^":
                if pointer == len(c)-1:
                    text += current_char
                    break
                # else, if the char at the next index is a digit, then it's a single digit color code
                # advance the pointer 2 steps
                elif c[pointer+1].isdigit():
                    pointer +=2
                # else, if the char at the next index to the carat is "x" which indicates it's a hex color code
                # extract the color code from the string at that index
                elif c[pointer+1] == "x":
                    color = c[pointer+2:pointer+5]
                    # if the length of the extracted color code is 3 check if it's a valid hex value
                    # if true advance pointer 5 steps
                    if len(color) == 3:
                        try:
                            if int(color, 16) < 4096:
                                pointer += 5
                        # if there is an error, mainly due to color not being a valid hex value
                        # add current char to the text string, advance pointer 1 step
                        except:
                            text += current_char
                            pointer += 1
                    # if the length of the color code is not 3 then add it to text string, advance pointer 1 step
                    else:
                        text += current_char
                        pointer += 1
                # if the char next to ^ isn't any color code indicator add current char to text, advance pointer 1 step
                else:
                    text += current_char
                    pointer += 1
            # if current char is not ^ add it to text, advance pointer 1 step
            else:
                text += current_char
                pointer += 1
    # return the filtered string
    return text


def norm(a):
    """
    Normalizes RGB values
    """
    f = lambda x : x/255

    r = f(a[0])
    g = f(a[1])
    b = f(a[2])

    return (r, g, b)

def denorm(a):
    """
    denormalizes rgb values
    """
    f = lambda x: int(x * 255)
    r = f(a[0])
    g = f(a[1])
    b = f(a[2])

    return (r, g, b)


#======================================#
# HSL Colorspace
#======================================#

# HSL to RGB
def hsl2rgb(h, s, l):
    """
    Converts HSL colorspace to RGB colorspace
    """
    # normalizing
    h /= 360
    s /= 100
    l /= 100

    if s == 0:
        r = g = b = l * 255
    else:
        if l < 0.5:
            q = l * (1 + s)
        else:
            q = l + s - l * s
        p = 2 * l - q

        r = hue2rgb(p, q, h + 1/3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h - 1/3)

    return (round(r * 255), round(g * 255), round(b * 255))

def hue2rgb(p, q, t):
    if t < 0:
        t += 1
    elif t > 1:
        t -= 1

    if t < 1/6:
        return p + (q - p) * 6 * t
    elif t < 1/2:
        return q
    elif t < 2/3:
        return p + (q - p) * (2/3 - t) * 6
    else:
        return p


