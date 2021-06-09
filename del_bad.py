import os

h264 = []
mp4 = []
for r, d, f in os.walk(os.getcwd()):
    for file in f:
        if file.endswith(".h264"):
            h264.append(os.path.join(r, os.path.splitext(file)[0]))
        if file.endswith(".mp4"):
            mp4.append(os.path.join(r, os.path.splitext(file)[0]))

todel = [x for x in h264 if x in mp4]

print(len(h264))
print(len(mp4))
print(len(todel))

for file in todel:
    os.remove(file + ".h264")

os.remove(os.path.realpath(__file__))