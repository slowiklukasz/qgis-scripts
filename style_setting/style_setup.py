from qgis.core import QgsProject, QgsCoordinateReferenceSystem
import os

def set_gs_style(layer, path):
    #loading STYLEs
    layer.loadNamedStyle(path)
    layer.triggerRepaint()
    
    #setting ENCODING
    layer.setProviderEncoding(u'UTF-8')
    layer.dataProvider().setEncoding(u'UTF-8')
    
    #setting COORDINATE SYSTEM TO EPGS 2178
    #layer.setCrs(QgsCoordinateReferenceSystem(2178, QgsCoordinateReferenceSystem.EpsgCrsId))
    
names = ["NAME1A", "NAME2A", "NAME1B", "NAME2B", "NAME1C", "NAME2C", "NAME3", \
	"name1a", "name2a", "name1b", "name2b", "name1c", "name2c", "name3"]

for layer in QgsProject.instance().mapLayers().values():
    for name in names:
        if layer.name().find(name) != -1:
            path = db_path = os.getcwd() + r"\styles\{}.qml".format(name)
            print(path)
            set_gs_style(layer, path)
        

