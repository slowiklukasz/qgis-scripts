from qgis.core import QgsProject, QgsCoordinateReferenceSystem
import os
import glob

path =r'2021'

for sdir in os.walk(path):
    group = sdir[0][len(path)+1:].replace('-','/')
    #group = sdir[0][45:].replace('-','/')
    root = QgsProject.instance().layerTreeRoot()
    myGroup = root.addGroup(group)

    for fn in glob.glob(r'{}\*.shp'.format(sdir[0])):
        if fn.endswith('.shp'):
            vlayer = QgsVectorLayer(fn, f'{os.path.basename(fn)}', "ogr")
            if not vlayer.isValid():
                print("Layer failed to load!")
            else:
                QgsProject.instance().addMapLayer(vlayer)
                layer = root.findLayer(vlayer.id())
                clone = layer.clone()
                myGroup.insertChildNode(0, clone)
                root.removeChildNode(layer)
                
                '''
                lyr=QgsProject.instance().addMapLayer(vlayer)
                myGroup.insertChildNode(1, QgsLayerTreeLayer(lyr))'''
