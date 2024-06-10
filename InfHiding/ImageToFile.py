from PIL import Image
from os.path import exists, split
from math import floor, sqrt
from concurrent.futures import ThreadPoolExecutor as TPE, as_completed


def error():
    print("The image content is wrong")
    exit()


# Enter image file path
filePath = input("File path:")
try:
    if filePath[-4:] != ".png":
        raise TypeError
    image = Image.open(filePath)
except:
    print("Invalid file name")
    exit()

# Load the image
pixels = image.load()
width, height = image.size
if width != 300 or image.mode != "RGBA": error()

# Convert pixels to bytes
print("\033[?25l", end="")


def convert(i, startLine, n):
    global pixels, content
    for line in range(n):
        for x in range(300):
            r, g, b, a = pixels[x, startLine + line]
            content[i] += r.to_bytes() + g.to_bytes() + b.to_bytes() + a.to_bytes()


numOfThreads = floor(sqrt(height))  # Refers to normal thread
content = [b''] * numOfThreads
lPT = height // numOfThreads   # Number of lines allocated per thread
with TPE(numOfThreads) as executor:
    futures = []
    for i in range(numOfThreads):
        futures.append(executor.submit(convert, i, lPT * i, lPT))
    futures.append(executor.submit(convert, numOfThreads, lPT * numOfThreads - lPT, height % lPT))
    for future in as_completed(futures):
        pass  # Block the main thread until it completes
con = b''
for c in content: con += c

length = int.from_bytes(con[:12], "big")
index = con[13:].index(0x2f) + 13
try:
    fileName = con[13:index].decode("utf-8")
except:
    error()
    exit()

# Save file
i = 1
while True:
    if not exists(filePath[:len(filePath) - len(split(filePath)[-1])] + "/" + str(i) + fileName):
        with open(filePath[:len(filePath) - len(split(filePath)[-1])] + "/" + str(i) + fileName, "wb") as file:
            file.write(con[index + 1:index + 1 + length])
            break
    i += 1
print("\r\033[K\033[?25h\"%d%s\" saved"%(i, fileName))
