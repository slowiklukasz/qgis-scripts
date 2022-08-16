from osgeo import gdal
import numpy as np


gdal.UseExceptions()

fn_raster = r"C:\Users\lukas\Desktop\rozmowa\pytania\raster_clip.tif"

fns_shp = [
    r"C:\Users\lukas\Desktop\rozmowa\pytania\shp\polygon1.shp",
    r"C:\Users\lukas\Desktop\rozmowa\pytania\shp\polygon2.shp",
    r"C:\Users\lukas\Desktop\rozmowa\pytania\shp\polygon2.shp"
    ]

def clip_to_layer(fn_raster, fn_shp, fn_out):
    result = gdal.Warp( fn_out, \
                        fn_raster, \
                        cutlineDSName = fn_shp, \
                        cropToCutline = True, \
                        dstNodata = np.nan)
                        

for nb, fn in enumerate(fns_shp):
    clip_to_layer(fn_raster, fn, "{}_{}.tif".format(fn[:-4], nb))
    


