import time

def clip_layer(layer, mask, out_fn):
    processing.run("native:clip", 
    {'INPUT':layer.source(),
    'OVERLAY': mask.source(),
    'OUTPUT': out_fn})
    iface.addVectorLayer(out_fn, 'ciecie_{}'.format(layer.name()), 'ogr')


#**** INPUT SECTION ****#
lyrs = iface.mapCanvas().layers()
mask = 'zakres_wniosku'
out_cat = QFileDialog.getExistingDirectory()

#parent = iface.mainWindow()
#fn_mask, fn_ok = QFileDialog.getOpenFileName(parent,"Zasięg do przycięcia", 
#                            QgsProject.instance().homePath(),
#                            "Shape Files (*.shp)")
#out_cat = r'C:\Users\lslowik\Desktop\lm test\wyniki'


#**** CALCULATION SECTION ****#
start = time.time()

clip_lst = []
for lyr in lyrs:
    if isinstance(lyr, QgsVectorLayer):
        if lyr.sourceName() != mask:
            clip_lst.append(lyr)
        else:
            mask_layer = lyr

for lyr in clip_lst:
    
    out_fn = '{}\\clip_{}.shp'.format(out_cat, lyr.name())
    print(out_fn)
    clip_layer(lyr, mask_layer, out_fn)

stop = time.time()
print('Calculated in {} seconds'.format(round(stop-start),2))
