import math
from qgis.core import QgsProject, QgsCoordinateReferenceSystem

''' NAZWA I ŚCIEŻKA DO WARSTWY WYNIKOWEJ'''
##### NAZWA WARSTWY WYNIKOWEJ #####
file_name='P1_do_wgrania'
##### ŚCIEŻKA DO WARSTWY WYNIKOWEJ #####
path=r'C:\DO_WGRANIA\{}.shp'.format(file_name)

''' WYSZUKIWANIE POWTARZAJĄCYCH SIĘ TAGÓW'''
layer = iface.activeLayer()
features=layer.getFeatures()

selected_fid=[]
tag_list=[]

for feature in features:
    attrs = feature.attributes()
    tag=attrs[8]
    tag_list.append((tag,feature.id()))


rpt_list=[]
ind_list=[]
for tag,ind in tag_list:
    if tag in rpt_list:
        pass
    else:
        rpt_list.append(tag)
        ind_list.append(ind)
        
layer.select(ind_list)
layer.invertSelection()

''' ZAPIS POWTARZAJĄCYCH SIĘ ARBOTAGÓW DO NOWEJ WARSTWY '''
writer=QgsVectorFileWriter.writeAsVectorFormat(layer, path, 'utf-8',driverName='ESRI Shapefile', onlySelected=True)
selected_layer=iface.addVectorLayer(path,'','ogr')
del(writer)
layer.removeSelection()

''' EDYCJA WYNIKOWEJ WARSTWY '''
# ustawienie aktywnej warstwy
layer = QgsProject.instance().mapLayersByName(file_name)[0]
iface.setActiveLayer(layer)


# przesunięcie punktów do wsp. x,y=666,666
layer.selectAll()
selection = layer.selectedFeatures()
caps = layer.dataProvider().capabilities()

for feature in selection:
    #feature.setGeometry(QgsGeometry.fromWkt('POINT(666,666)'))
    #feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(666,666)))
    #feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(666,666)))
    if caps & QgsVectorDataProvider.ChangeGeometries:
        geom = QgsGeometry.fromPointXY(QgsPointXY(666,666))
        #geom = QgsGeometry.fromWkt('POINT(666,666)')
        layer.dataProvider().changeGeometryValues({ feature.id() : geom })


    
# zmiana wartości w kolumnie 'number tag'
res = layer.dataProvider().addAttributes([QgsField("ID_temp", QVariant.String)])
layer.updateFields()

expression1=QgsExpression('$id')
context=QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

with edit(layer):
    for feature in layer.getFeatures():
        # stworzenie columny 'ID_temp'
        context.setFeature(feature)
        feature['ID_temp']=expression1.evaluate(context)
        layer.updateFeature(feature)
        
        # zmiana wartości w kolumnie 'z', 'a','number tag','note'
        feature[2]=19
        feature[3]='666'
        feature[20]=feature[8]+' (tag)'
        feature[8]=str(feature[23])+'usun'
        layer.updateFeature(feature)
        
# usunięcie kolumny 'ID_temp'
layer.dataProvider().deleteAttributes([23])
layer.updateFields()
layer.removeSelection()

print('ZAKOŃCZONO')

#### SPRAWDZENIE W KALKULATORZE ####
''' 
1. count("note", group_by:="note")
2. Posortować po 'note', szukać powtórzeń innych niż 4 i sprawdzić ręcznie'''

