""" UWAGA: 

do wykonania poprawnych obliczeń koniecznym jest doprowadzenie 
przeliczanej kolumny do jednorodnej postaci - tj. drzewa wielopniowe oddzialami 
jednym ustalonym znakiem, opisanym poniżej jako "znacznik" (np. średnik, przecinek)
z uwaględnieniem spacji. 

PO WYKONANIU OBLICZEŃ MOŻE BYĆ KONIECZNYM ZRESETOWANIE PROJEKTU/PONOWNE WCZYTANIE
PRZELICZANEJ WARSTWY
"""


""" DANE DO PRZELICZENIA"""
##################################################

# 1. srednica -> NAZWA KOLUMNY Z ŚRENICAMI
# 2. obwod -> NAZWA NOWO UTWORZONEJ KOLUMNY Z OBWODAMI - JEŻELI JUŻ ISTNIEJE ZOSTANIE NADPISANA (MAX 10 ZNAKÓW)
# 3. znacznik ->ZNACZNIK ODZIELAJĄCY W DRZEWACH WIELOPNIOWYCH 

srednica = "srednica"
obwod = "obwod"
znacznik = ";"

##################################################




""" NIE ZMIENIAĆ TEKSTU PONIŻEJ!"""
"""PRZELICZENIE ŚREDNIC NA OBWODY Z UWZGLĘDNIENIEM DRZEW WIELOPNIOWYCH"""
import math
import time
from qgis.core import QgsProject, QgsCoordinateReferenceSystem


fn, fn_ok = QFileDialog.getOpenFileName(iface.mainWindow(), \
                            "Plik P1.shp do przeliczenia", 
                            QgsProject.instance().homePath(),
                            "Shape Files (*.shp)")
if fn_ok:
    start = time.time()

    layer = QgsVectorLayer(fn, "P1", "ogr")
    layer.startEditing()

    # SPRAWDZENIE CZY WARSTWA ZWAWIERA ODPOWIDNIĄ KOLUMNĘ/STWORZENIE NOWEJ KOLUMNY
    idx = layer.fields().indexOf(obwod)

    if idx == -1:
        new_fld = QgsField(obwod, QVariant.String, len = 80)
        layer.dataProvider().addAttributes([new_fld])
        layer.updateFields()
        print(f"Dodano kolumnę: {obwod}")

    # PRZELICZENIE OBWODU ORAZ DOPISANIE GO DO NOWEJ KOLUMNY
    print("Kalkulacja...")
    features = layer.getFeatures()
    for feature in features:
        sred = feature[srednica]
        codice = feature["codice"]
        
        obw = ""
        
        if codice in ('P103108', 'P103118') and sred:
            if znacznik in sred:
                for i in sred.split(znacznik):
                    tmp = round(float(i)* math.pi)
                    obw += "{};".format(tmp)
                    feature[obwod] = obw[:-1]
            else:
                feature[obwod] = str(round(float(sred) * math.pi))
                
            layer.updateFeature(feature)
            
    layer.commitChanges()
    layer.reload()

    stop = time.time()
#    iface.addVectorLayer(fn, "przeliczone", "ogr")
    print("Zakończono w: {}".format(round(stop - start)))
    QMessageBox.warning(iface.mainWindow(), "Wykonano", "Obliczone w: {} sek".format(round(stop - start)))

else:
    QMessageBox.warning(iface.mainWindow(), "", "Nie wybrano pliku")