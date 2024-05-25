from PIL import Image
from os.path import exists, split

filePath = input("File path:")
try:
    with open(filePath, "rb") as file:
        content = file.read()
        # Add the file size and name to the header for later decoding
        content = len(content).to_bytes(12) + b'/' + split(filePath)[-1].encode("utf-8") + b'/' + content
except:
    print("Invalid file name")
    exit()

def temp(i):
    if i: return 1
    return 0

length = len(content)
height = length // 4  + temp(length % 4)
height = height // 300 + temp(height % 300)
image = Image.new("RGBA", (300, height), (0, 0, 0, 0))

for i in range(length):
    i += 1
    y = i // 4 + temp(i % 4)
    x = y % 300
    y = y // 300 + temp(y % 300)
    p = i % 4
    if p == 0: p = 4
    p -= 1
    pixel = image.getpixel((x-1, y-1))
    pixel = [pixel[0], pixel[1], pixel[2], pixel[3]]
    pixel[p] = content[i - 1]
    image.putpixel((x-1, y-1), (pixel[0], pixel[1], pixel[2], pixel[3]))

i = 1
while True:
    if not exists(filePath[:len(filePath)-len(split(filePath)[-1])] + "/%d.png"%i):
        image.save(filePath[:len(filePath)-len(split(filePath)[-1])] + "/%d.png"%i)
        break
    i += 1
print("\"%d\".png saved"%i)
