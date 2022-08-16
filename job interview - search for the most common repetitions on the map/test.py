import numpy as np
from osgeo import gdal


fns = [
    r"C:\Users\lukas\Desktop\rozmowa\pytania\raster_clip.tif",
    r"C:\Users\lukas\Desktop\rozmowa\pytania\polygon1_0.tif",
    r"C:\Users\lukas\Desktop\rozmowa\pytania\polygon2_1.tif",
    r"C:\Users\lukas\Desktop\rozmowa\pytania\polygon2_2.tif"
    ]

fn_out = r"C:\Users\lukas\Desktop\rozmowa\pytania\output.tif"

def get_x_y(fn):
    ds = gdal.Open(fn)
    
    x_size = ds.RasterXSize
    y_size = ds.RasterYSize
    
    transform = ds.GetGeoTransform()
    x_min = transform[0]
    x_max = transform[0] + transform[1] * x_size
    y_min = transform[3]
    y_max = transform[3] + transform[5] * y_size
    
#    lyr = QgsRasterLayer(fn, "Name", "gdal")
#    print(lyr.width(), ds.RasterXSize)
#    print(lyr.height(), ds.RasterYSize)
#    print(ds.RasterYSize * transform[5])
    
    ds = None
    return (x_min, x_max, y_min, y_max)

x_lst = []
y_lst = []

for fn in fns:
    res = get_x_y(fn)
#    print(res)
#    print(res[1]-res[0])
#    print(res[3]-res[2])
    x_lst.extend([res[0], res[1]])
    y_lst.extend([res[2], res[3]])

x_min = min(x_lst)
x_max = max(x_lst)
y_min = min(y_lst)
y_max = max(y_lst)

# CREATING NEW RASTER
ds = gdal.Open(fns[0])
transform = ds.GetGeoTransform()
pixel_x_size = transform[1]
pixel_y_size = transform[5]

new_geot = [x_min, pixel_x_size, 0, y_max, 0, pixel_y_size]

driver_tif = gdal.GetDriverByName('GTiff')
new_ds = driver_tif.Create( fn_out, 
                            int((x_max-x_min)/transform[1]), 
                            abs(int((y_max-y_min)/transform[5])), 
                            bands = 1, 
                            eType = gdal.GDT_Float32)

new_ds.SetGeoTransform(new_geot)
new_ds.SetProjection(ds.GetProjection())

tmp_data = np.zeros((ds.RasterYSize, ds.RasterXSize))



for fn in fns:
    ds = gdal.Open(fn)
    data = ds.GetRasterBand(1).ReadAsArray()
    x_size = ds.RasterXSize
    y_size = ds.RasterYSize
    transform = ds.GetGeoTransform()
    
    x_offset = int((transform[0] - new_geot[0])/transform[1])
    y_offset = int((transform[3] - new_geot[3])/transform[5])
    
    print(data.shape)
    print(tmp_data.shape)
    
    print(x_offset, x_size)
    
    tmp_data[y_offset:y_offset + y_size, x_offset:x_offset + x_size] += data
    ds = None
    
print(tmp_data)
new_ds.GetRasterBand(1).WriteArray(tmp_data)

new_ds = None



measurements = 10
propability = 0.1
treshold = 3

x_block_size = 3
y_block_size = 2

x_size = 15
y_size = 10


def random_data():
    data = np.zeros((y_size,x_size))

    rows = data.shape[0]
    cols=data.shape[1]

    for r in range(rows):
        for c in range(cols):
            rn = np.random.choice(np.arange(0,2), p=[1 - propability, propability])
            data[r, c] = rn
    return data
    
sum_data = np.zeros((y_size,x_size))

for i in range(measurements):
    data = random_data()
    sum_data += data
    
print(sum_data)
print(np.max(sum_data))


print("VAR 1 - SUMMING QUANTITIES BY COORDINATES")
res = np.where(sum_data >=treshold)
#res = np.where(sum_data == np.max(sum_data))
data_noise = np.where(sum_data == measurements)

if len(data_noise[0])>0:
    print("DATA NOISE: \ny, x")
    for y,x in zip(data_noise[0], data_noise[1]):
        print(y,x)
    print("="*10)
        
if len(res)>0:
    print("VISITED OVER {} TIMES:".format(treshold))
    print(res)
    print("y, x:")
    for y,x in zip(res[0], res[1]):
        print(y,x)


print("\nVAR 2 - SUMMING QUANTITIES USING SPECIFIED BLOCKS")
blocks = {}
nb = 0
for i in range(0, x_size, x_block_size):
    if i + x_block_size < x_size:
        cols = x_block_size
    else:
        cols = x_size - i
        
    for j in range(0, y_size, y_block_size):
        if j + y_block_size < y_size:
            rows = y_block_size
        else:
            rows = y_size - j
            
        nb+=1
            
#        block = band.ReadAsArray(i, j, numCols, numRows)
        block = sum_data[j:j+rows, i:i+cols]
        
        sum = np.sum(block)
        blocks[sum] = (nb, block)
        
for k in sorted(blocks, reverse = True):
#    print(k, blocks[k])
    print("-"*10)
    print("Block number: {}".format(blocks[k][0]))
    print("Block sum : {}".format(k))
    print("Block:\n{}".format(blocks[k][1]))