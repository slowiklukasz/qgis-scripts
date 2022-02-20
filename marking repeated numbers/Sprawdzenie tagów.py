import math
from qgis.core import QgsProject, QgsCoordinateReferenceSystem

''' WYSZUKIWANIE POWTARZAJĄCYCH SIĘ TAGÓW'''
# ścieżka do wynikowego .txt
path=r'C:\powtorki_tagow\powtorki.txt'

with open(path, 'w') as f:
    for layer in QgsProject.instance().mapLayers().values():
        if layer.name().find('P1') != -1:

            features=layer.getFeatures()
            tag_list=[]
            for feature in features:
                attrs = feature.attributes()
                tag=attrs[8]
                tag_list.append(tag)
                
            rpt_list=[]
            f.write('Tag\t|Liczba powtórzeń\n')    
            for i in tag_list:
                if tag_list.count(i)>1 and rpt_list.count(i)==0:
                    rpt_list.append(i)
                    f.write('{}\t|{}\n'.format(i,tag_list.count(i)))
                    
        print(f'Liczba powtórek: {len(rpt_list)}')


