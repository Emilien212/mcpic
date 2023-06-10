import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

files = os.listdir("./textures")

db = {}

for file in files:
    dir = f"./textures/{file}"
    image = Image.open(dir)
    
    data = np.asarray(image)/255 # load image in numpy array
    data = np.delete(data, -1, axis=2) # remove transparancy
    data_r = data.reshape(256, 3) # flatten image
    avg = np.sum(data_r, axis=0)/256
    
    db[dir] = avg

for d in os.listdir("./data"):
    dir = f"./data/{d}"
    image = Image.open(dir)
    image = image.convert("RGB")
    data = np.asarray(image)/255
    shape = np.shape(data)

    data = data[shape[0]%16:, shape[1]%16:] # make height and width divisble by 16
    shape = np.shape(data)

    final = np.zeros_like(data)

    def distance(a, b):
        sum = 0
        for i in range(len(a)):
            sum += (a[i] - b[i])**2
        return sum

    for m in range(shape[0]//16):
        for n in range(shape[1]//16):
            block = data[m*16:(m+1)*16, n*16:(n+1)*16, :]
            avg = np.sum(block.reshape(256, 3), axis=0)/256

            min = 3
            path = 0
            for key in db.keys():
                dist = distance(avg, db[key])
                if dist < min : 
                    min = dist 
                    path = key
            
            image = np.asarray(Image.open(path))/255
            image = np.delete(image, -1, axis=2)
            final[m*16:(m+1)*16, n*16:(n+1)*16, :] = image

    image = Image.fromarray((final * 255).astype(np.uint8))
    image.save(f"./output/{os.path.splitext(d)[0]}.png")