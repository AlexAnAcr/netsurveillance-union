import os

mp4 = []
for r, d, f in os.walk(os.getcwd()):
    for file in f:
        if file.endswith(".mp4"):
            if os.path.getsize(os.path.join(r, file)) == 0:
                mp4.append(os.path.join(r, file))

for file in mp4:
    print(file)
    os.remove(file)

os.remove(os.path.realpath(__file__))