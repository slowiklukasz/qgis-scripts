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
# 1. obwod -> NAZWA KOLUMNY Z OBWODAMI
# 2. srednica -> NAZWA NOWO UTWORZONEJ KOLUMNY Z ŚRENICAMI - JEŻELI JUŻ ISTNIEJE ZOSTANIE NADPISANA (MAX 10 ZNAKÓW)
# 3. znacznik ->ZNACZNIK ODZIELAJĄCY W DRZEWACH WIELOPNIOWYCH
# 4. znacznik2 -> ZNACZNIK ODZIELAJĄCY W DRZEWACH WIELOPNIOWYCH (OPCJONALNY)

obwod = "obwod"
srednica = "srednica"
znacznik1 = ", "
znacznik2 = ";"

##################################################



""" NIE ZMIENIAĆ TEKSTU PONIŻEJ!"""
""" SKRYPT - PRZELICZENIE OBWODÓW NA ŚREDNICE Z UWZGLĘDNIENIEM DRZEW WIELOPNIOWYCH"""
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

    # SPRAWDZENIE CZY WARSTWA ZWAWIERA ODPOWIEDNIĄ KOLUMNĘ/STWORZENIE NOWEJ KOLUMNY
    idx = layer.fields().indexOf(srednica)

    if idx == -1:
        new_fld = QgsField(srednica, QVariant.String, len = 80)
        layer.dataProvider().addAttributes([new_fld])
        layer.updateFields()
        print("Dodano kolumnę: {}".format(srednica))

    # PRZELICZENIE ŚREDNICY ORAZ DOPISANIE GO DO NOWEJ KOLUMNY
    print("Kalkulacja...")
    features = layer.getFeatures()
    for feature in features:
        obw = feature[obwod]
        codice = feature["codice"]
        
        sred = ""
        
        if codice in ('P103108', 'P103118') and obw:
            if znacznik1 in obw:
                for i in obw.split(znacznik1):
                    tmp = round(float(i)/ math.pi)
                    sred += "{};".format(tmp)
                    feature[srednica] = sred[:-1]
        
            elif znacznik2 in obw:
                for i in obw.split(znacznik2):
                    tmp = round(float(i)/ math.pi)
                    sred += "{};".format(tmp)
                    feature[srednica] = sred[:-1]
            else:
                feature[srednica] = str(round(float(obw)/math.pi))
                
            layer.updateFeature(feature)
            
    layer.commitChanges()

    stop = time.time()
#    iface.addVectorLayer(fn, "przeliczone", "ogr")
    print("Zakończono w: {}".format(round(stop - start)))
    QMessageBox.warning(iface.mainWindow(), "Wykonano", "Obliczone w: {} sek".format(round(stop - start)))

else:
    QMessageBox.warning(iface.mainWindow(), "", "Nie wybrano pliku")