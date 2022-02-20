import math
from qgis.core import QgsProject, QgsCoordinateReferenceSystem

''' SKRYPT PRZELICZA OBWODY PODANE W KOLUMNIE 'SREDNICE' I UMIESZCZA JE W NOWEJ KOLUMNIE ('OBWOD' - TYP STRING).  
UWGLĘDNIONE ZOSTAJĄ DRZEWA WIELOPNIOWE, OBWÓD LICZONY JAKO SUMA OBWODU NAJGRUBSZEGO PNIA ORAZ POŁOWA OBWODÓW POZOSTAŁYCH'''

for layer in QgsProject.instance().mapLayers().values():
    if layer.name().find('P1') != -1:
        layer.startEditing()
        
        # SPRAWDZENIE CZY WARSTWA ZWAWIERA ODPOWIDNIĄ KOLUMNĘ/STWORZENIE NOWEJ KOLUMNY
        idx = layer.fields().indexOf('Obwod')
        if idx != -1:
            print('\n#############################')
            print('Field "Obwod" found!\nCalculating...')
            print('')
        else:
            myField = QgsField('Obwod', QVariant.Double)
            print('\n#############################')
            print('Column "Obwod" added\nCalculating...')
            layer.dataProvider().addAttributes([myField])
            layer.updateFields()

        # PRZELICZENIE OBWODU ORAZ DOPISANIE GO DO NOWEJ KOLUMNY
        features=layer.getFeatures()
        for feature in features:
            list=[]
            attrs = feature.attributes()
            
            code = attrs[7]
            tag = attrs[8]
            diam_tronc = attrs[13]
            obwod = attrs[23]

            if code =='103108' and diam:
                if ';' in diam_tronc:
                    tmp_list=[float(x) for x in diam.split(';')]
                    sum=0
                    for i in tmp_list:
                        if i==max(tmp_list):
                            sum+=i*math.pi
                        else:
                            sum+=i*math.pi*1/2
                    obw=str(round(sum,2))
                elif ';' not in diam_tronc:
                    sum=float(diam_tronc)*math.pi
                    obw=str(round(sum,2))
            elif code !='P103108' or not diam:
                obw=''

            feature['Obwod']=obw
            layer.updateFeature(feature)
                
        layer.commitChanges()
        print('ZAKOŃCZONO')
        print('#############################')
