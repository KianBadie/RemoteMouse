# RemoteMouse

This is a program to control the computer mouse through a mobile browser on the same local network written mostly in Python.

`requirements.txt` is not up to date. There are unnecessary files in there.

## Resources

I did not write the servers from scratch. I learned a lot from the resources listed below. I used these resources to heavily model/inspire my code and built upon them to implement the features I wanted to.

- https://ruslanspivak.com/lsbaws-part1/ - I used part 1 and part 2 of the "Let's Build A Web Server" series written by Ruslan Spivak. It helped me learn some basics about WSGI and how to connect HTTP servers and WSGI apps. The `rmServer.py` follows the server he creates pretty closely, and the `rmApp.py` is modeled after the custom WSGI app he creates as well.
- https://websockets.readthedocs.io/en/stable/index.html - I used the "Basic Example" in the Getting Started section of this Python websockets module in a similar fashion. `socketServer.py` almost builds directly on top of it. The part I modified is what is done with the data after it is received.
