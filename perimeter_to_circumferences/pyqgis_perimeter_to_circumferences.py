import math
import time
from qgis.core import QgsProject, QgsCoordinateReferenceSystem

"""PRZELICZENIE ŚREDNIC NA OBWODY Z UWZGLĘDNIENIEM DRZEW WIELOPNIOWYCH"""

fn, fn_ok = QFileDialog.getOpenFileName(iface.mainWindow(), \
                            "Plik P1.shp do przeliczenia", 
                            QgsProject.instance().homePath(),
                            "Shape Files (*.shp)")
if fn_ok:
    start = time.time()

    layer = QgsVectorLayer(fn, "P1", "ogr")
    layer.startEditing()

    # SPRAWDZENIE CZY WARSTWA ZWAWIERA ODPOWIDNIĄ KOLUMNĘ/STWORZENIE NOWEJ KOLUMNY
    idx = layer.fields().indexOf("Obwod")

    if idx == -1:
        new_fld = QgsField("Obwod", QVariant.String, len = 80)
        layer.dataProvider().addAttributes([new_fld])
        layer.updateFields()
        print("Dodano kolumnę: 'Obwod'")

    # PRZELICZENIE OBWODU ORAZ DOPISANIE GO DO NOWEJ KOLUMNY
    perim_tronc = ""
    features = layer.getFeatures()
    for feature in features:
        diam_tronc = feature["diam_tronc"]
        codice = feature["codice"]
        
        perim_tronc = ""
        
        if codice=='P103108' and diam_tronc:
            if ';' in diam_tronc:
                for i in diam_tronc.split(';'):
                    tmp = round(float(i)* math.pi)
                    perim_tronc += "{};".format(tmp)
                    feature["Obwod"] = perim_tronc[:-1]
            else:
                feature["Obwod"] = str(round(float(diam_tronc) * math.pi))
                
            layer.updateFeature(feature)
            
    layer.commitChanges()

    stop = time.time()
    iface.addVectorLayer(fn, "przeliczone", "ogr")
    QMessageBox.warning(iface.mainWindow(), "Wykonano", "Obliczone w: {} sek".format(stop - start))

else:
    QMessageBox.warning(iface.mainWindow(), "Uwaga", "Nie wybrano pliku")