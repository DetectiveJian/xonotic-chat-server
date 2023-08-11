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

#------------------------------------------------------------------------------------------------------#

# Author: tofh
# Last Updated: 10-08-2023
# Description: xonotic-chat-server is inspired by shazza-work's amazing xonotic_colour project.

#------------------------------------------------------------------------------------------------------#


from flask import Flask, request
from utils import *
import libcolors

# Server listening for requests
app = Flask(__name__)

@app.route("/server", methods=["GET"])
def server():
    """
    Server listening for queries
    """
    # http:127.0.0.1:5000/server?query=<cmd><stuff>

    # filter all the xonotic color codes from the query
    query = libcolors.xonfilter(request.args.get("query"))
    print(f"[query] {query}")

    # random rainbow colors
    if query.startswith("!randbow"):
        text = query.removeprefix("!randbow")
        return "say " + rand_rainbow_encode(text)

    # rainbow colors
    elif query.startswith("!rainbow"):
        text = query.removeprefix("!rainbow")
        return "say " + rainbow_encode(text)

    # random colors
    elif query.startswith("!randcolor"):
        text = query.removeprefix("!randcolor")
        return "say " + rand_color_encode(text)

    # user defined colors
    elif query.startswith("!color"):
        data = query.removeprefix("!color").split("@", 2)
        if len(data) > 2:
            text = data[-1].strip()
            start = data[0].strip()
            stop = data[1].strip()

            if validColorCode(start):
                if validColorCode(stop):
                    return "say " + color_encode(text, start, stop)
                else:
                    return f"echo ^7[^2COLOR ENCODE^7]^3 INVALID STOP COLOR CODE^7: ^1{stop}^7 ^3in ^2{query}^7"
            else:
                return f"echo ^7[^2COLOR ENCODE^7]^3 INVALID START COLOR CODE^7: ^1{start}^7 ^3in ^2{query}^7 "
        else:
            return f"echo ^7[^2COLOR ENCODE^7]^3 INVALID NO. OF ARGUMENTS^7: ^1{query}^7"

    # display help in xonotic's console
    elif query.startswith("!help"):
        return help()

    elif query.startswith("!ping"):
        return "echo ^1RESPONSE:^2 pong"

    # if none of the above requests, tell user the query is invalid
    else:
        return f"echo ^1INVALID REQUEST:^2 {query}^7"

if __name__ == "__main__":
    app.run()
