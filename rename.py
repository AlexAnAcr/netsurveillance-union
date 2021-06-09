import os

files = []
for r, d, f in os.walk(os.getcwd()):
    for file in f:
        if not file.endswith(".py"):
            files.append(os.path.join(r, file))

def ReplacePath(inp):
    s = ""
    s += inp[6:10]
    s += "."
    s += inp[10:12]
    s += "."
    s += inp[12:14]
    s += " "
    s += inp[15:17]
    s += "-"
    s += inp[17:19]
    s += "-"
    s += inp[19:21]
    return s

for f in files:
    os.rename(f, os.path.dirname(f) + "\\" + ReplacePath(os.path.splitext(os.path.basename(f))[0]) + os.path.splitext(f)[1])

os.remove(os.path.realpath(__file__))