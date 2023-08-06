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
# Last Updated: 06-08-2023
# Description: xonotic-chat-server is inspired by shazza-work's amazing xonotic_colour project.

#------------------------------------------------------------------------------------------------------#


from flask import Flask, request
import utils
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

    response = ""

    # look for commands
    # if the request is !say, send back the data as is
    if query.startswith("!say"):
        data = query.removeprefix("!say")
        response = f"say {data}"

    # add colors to the data specified by the user
    # example: !coolor fff# 000# Hello, world!
    elif query.startswith("!color"):
        data = query.removeprefix("!color").split("@", 2)
        if len(data) == 3:
            color = [data[0].strip(), data[1].strip()]
            text = data[2]
            response = "say " + utils.color(text, option="color", extra=color)
        else:
            response = "echo ^1RESPONSE: ^7[^2!color^7] ^3INVALID DATA PROVIDED^7"

    # display help in xonotic's console
    elif query.startswith("!help"):
        response = utils.help()

    elif query.startswith("!ping"):
        response = "echo ^1RESPONSE:^2 pong"

    # if none of the above requests, tell user the query is invalid
    else:
        response = f"echo ^1INVALID REQUEST:^2 {query}^7"
    return response

if __name__ == "__main__":
    app.run()
