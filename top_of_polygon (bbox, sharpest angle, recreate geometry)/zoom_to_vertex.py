# zooming to selected vertex - checking recreate_geometry.py result

idx = 0

mc = iface.mapCanvas()
lyr_in = mc.currentLayer()

for ftr_in in lyr_in.selectedFeatures():
    geom = ftr_in.geometry()
    poly = geom.asGeometryCollection()
    poly_vertices = poly[0].asPolygon()[0]
    
    v = poly_vertices[idx]
    
    cntr = QgsPointXY(v.x(), v.y())
    cntr = poly_vertices[idx]
    mc.setCenter(cntr)
    mc.zoomScale(100)