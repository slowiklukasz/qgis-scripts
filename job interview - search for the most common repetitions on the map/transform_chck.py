from osgeo import gdal

fn1 = r"C:\Users\lukas\Desktop\rozmowa\pytania\raster_clip.tif"
fn2 = r"C:\Users\lukas\Desktop\rozmowa\pytania\output.tif"

def read_transform(fn):
    ds = gdal.Open(fn)
    transform = ds.GetGeoTransform()
    ds = None
    print(transform)
    
read_transform(fn1)
read_transform(fn2)