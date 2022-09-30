import os
import math
from osgeo import gdal
import matplotlib.pyplot as plt
from scipy import ndimage


path = r"C:\"
os.chdir(path)


img_data = []

for r,d,fns in os.walk(path):
    print(fns)
    for fn in fns:
        if fn.endswith(".jpg"):
            fn = "{}\{}".format(path, fn)
            print(fn)
            ds = gdal.Open(fn)
            data = ds.GetRasterBand(1).ReadAsArray()
            img_data.append(data)
            ds = None
        
rows = math.ceil(len(img_data)/2)
cols = math.floor(len(img_data)/2)

fig = plt.figure(figsize=(100, 100))

for i in range(rows+cols):
    fig.add_subplot(rows, cols, i+1)
    rotated_img = ndimage.rotate(img_data[i], -90)
    plt.imshow(rotated_img, cmap="viridis")
    
    plt.axis('off')
    plt.title("{}".format(i))

plt.show()
        
    

    
    