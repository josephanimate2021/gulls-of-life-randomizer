import http.server
import socketserver
import os

PORT = 9000
Handler = http.server.SimpleHTTPRequestHandler

def make_bugfix_file(file):
    print(f"Creating bugfixes text file for {DIR_START}/{file}...")
    bugfixes = ""
    for f in os.listdir(f"{DIR_START}/{file}/bugfixes"):
        bugfixes += f + "\n"
    open(f"{DIR_START}/{file}/ages.txt", "w").write(bugfixes)
    print("Bugfixes file successfully created!")

DIR_START = "romhack_builds"
for file in os.listdir(DIR_START):
    if os.path.exists(f"{DIR_START}/{file}/bugfixes"):
        if not os.path.exists(f"{DIR_START}/{file}/ages.txt"):
            make_bugfix_file(file)
        contents = open(f"{DIR_START}/{file}/ages.txt").read().splitlines()
        dirlist = os.listdir(f"{DIR_START}/{file}/bugfixes")
        if len(contents) != len(dirlist):
            make_bugfix_file(file)
        for i in range(len(dirlist)):
            if contents[i] != dirlist[i]:
                make_bugfix_file(file)
                break

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
