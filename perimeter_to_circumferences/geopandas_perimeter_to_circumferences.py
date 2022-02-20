import geopandas as gpd
import math
import time

start = time.time()

in_fn = r"1.shp"
out_fn = r"new.shp"

lyr_trees = gpd.read_file(in_fn, encoding="latin-1")


def calc_raptor_perims(diam_tronc):
    if diam:
        perim = ""
        if ';' in diam:
            for i in diam.split(';'):
                tmp = round(float(i) * math.pi)
                perim_tronc += "{};".format(tmp)
            return perim[:-1]
        else:
            perim = str(round(float(diam) * math.pi))
            return perim


lyr_trees["perim"] = lyr_trees["diam"].apply(calc_raptor_perims)
lyr_trees.to_file(out_fn)
# lyr_trees[lyr_trees["code"] == "103108"].to_file(out_fn,  encoding='utf-8')

stop = time.time()

print("Done in: {}".format(stop - start))
