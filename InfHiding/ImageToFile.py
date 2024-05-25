from PIL import Image
from os.path import exists, split


def errHandling():
    print("The image content is wrong")
    exit()


filePath = input("File path:")
try:
    if filePath[-4:] != ".png":
        raise TypeError
    image = Image.open(filePath)
except:
    print("Invalid file name")
    exit()

pixels = image.load()
width, height = image.size
if width != 300: errHandling()

content = b''
for y in range(height):
    for x in range(300):
        r, g, b, a = pixels[x, y]
        content += r.to_bytes() + g.to_bytes() + b.to_bytes() + a.to_bytes()

length = int.from_bytes(content[:12], "big")
index = content[13:].index(0x2f) + 13
fileName = content[13:index].decode("utf-8")

i = 1
while True:
    if not exists(filePath[:len(filePath)-len(split(filePath)[-1])] + "/" + str(i) + fileName):
        with open(filePath[:len(filePath)-len(split(filePath)[-1])] + "/" + str(i) + fileName, "wb") as file:
            file.write(content[index+1:index+1+length])
            break
    i += 1
print(str(i) + fileName + " saved")
