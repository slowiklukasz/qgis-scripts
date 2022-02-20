import geopandas as gpd
import math
import time

start = time.time()

in_fn = r"C:\Users\lukas\Desktop\przeliczanie obwodów\ZASOB_GS\P1.shp"
out_fn = r"C:\Users\lukas\Desktop\wnk\P1_new.shp"

lyr_trees = gpd.read_file(in_fn, encoding="latin-1")


def calc_raptor_perims(diam_tronc):
    if diam_tronc:
        perim_tronc = ""
        if ';' in diam_tronc:
            for i in diam_tronc.split(';'):
                tmp = round(float(i) * math.pi)
                perim_tronc += "{};".format(tmp)
            return perim_tronc[:-1]
        else:
            perim_tronc = str(round(float(diam_tronc) * math.pi))
            return perim_tronc


lyr_trees["diam_perim"] = lyr_trees["diam_tronc"].apply(calc_raptor_perims)
lyr_trees.to_file(out_fn)
# lyr_trees[lyr_trees["codice"] == "P103108"].to_file(out_fn,  encoding='utf-8')

stop = time.time()

print("Done in: {}".format(stop - start))
