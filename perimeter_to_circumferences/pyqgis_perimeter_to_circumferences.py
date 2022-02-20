import math
import time
from qgis.core import QgsProject, QgsCoordinateReferenceSystem

"""PRZELICZENIE ŚREDNIC NA OBWODY Z UWZGLĘDNIENIEM DRZEW WIELOPNIOWYCH"""

fn, fn_ok = QFileDialog.getOpenFileName(iface.mainWindow(), \
                            "Plik name1.shp do przeliczenia", 
                            QgsProject.instance().homePath(),
                            "Shape Files (*.shp)")
if fn_ok:
    start = time.time()

    layer = QgsVectorLayer(fn, "name1", "ogr")
    layer.startEditing()

    # SPRAWDZENIE CZY WARSTWA ZWAWIERA ODPOWIDNIĄ KOLUMNĘ/STWORZENIE NOWEJ KOLUMNY
    idx = layer.fields().indexOf("Obwod")

    if idx == -1:
        new_fld = QgsField("Obwod", QVariant.String, len = 80)
        layer.dataProvider().addAttributes([new_fld])
        layer.updateFields()
        print("Dodano kolumnę: 'Obwod'")

    # PRZELICZENIE OBWODU ORAZ DOPISANIE GO DO NOWEJ KOLUMNY
    features = layer.getFeatures()
    for feature in features:
        diam = feature["diam"]
        code = feature["code"]
        
        perim = ""
        
        if code=='103108' and diam:
            if ';' in diam:
                for i in diam.split(';'):
                    tmp = round(float(i)* math.pi)
                    perim += "{};".format(tmp)
                    feature["perim"] = perim_tronc[:-1]
            else:
                feature["perim"] = str(round(float(diam_tronc) * math.pi))
                
            layer.updateFeature(feature)
            
    layer.commitChanges()

    stop = time.time()
    iface.addVectorLayer(fn, "przeliczone", "ogr")
    QMessageBox.warning(iface.mainWindow(), "Wykonano", "Obliczone w: {} sek".format(stop - start))

else:
    QMessageBox.warning(iface.mainWindow(), "Uwaga", "Nie wybrano pliku")