from PIL import Image
import numpy as np
import os

for name in os.listdir("./textures"):
    dir = f"./textures/{name}"
    if os.path.splitext(dir)[1] != ".png":
        os.remove(dir)
        print(dir)
        continue

    image = Image.open(dir)
    data = np.asarray(image)
    if np.shape(data) != (16, 16, 4):
        os.remove(dir)
        print(dir)
    else:
        flag = True
        for m in data:
            if not flag:
                break
            for n in m:
                if (n == np.array([0, 0, 0, 0])).all(): 
                    os.remove(dir)
                    print(dir)
                    flag = False
                    break
