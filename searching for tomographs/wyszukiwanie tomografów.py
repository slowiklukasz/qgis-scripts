import glob
import os

lat = "50.058795"
lng = "19.940323"

cat = r"C:\Users\l...\Desktop\_PiT"
fns = r"{}\*.PIT".format(cat)


parent = iface.mainWindow()
mc = iface.mapCanvas()


int, b_ok = QInputDialog.getDouble(parent, "Title", "Prompt", 7, 1, 10, 1)
if b_ok:
    print(int)
else:
    print("User canceled")



fns_lst  = []

for fn in glob.glob(fns):
    fns_lst.append(fn)


for i in fns_lst:
    with open(i, "r") as f:
        content = f.read()
        if "Longitude={}".format(lng) and \
       "Latitude={}".format(lat) in content:
            print(i)