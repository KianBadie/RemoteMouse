import sys
import fileinput

HOST = sys.argv[2]
PORT = int(sys.argv[1])

lines = []
with open('socketPage.html', 'r') as page:
        lines = page.readlines()

# Search for the line where the websocket is created
for i in range(0, len(lines)):
    if 'let socket =' in lines[i].strip():
        lines[i] = f'\t\tlet socket = new WebSocket("ws://{HOST}:{PORT}");\n'

with open('socketPage.html', 'w') as page:
    page.writelines(lines)