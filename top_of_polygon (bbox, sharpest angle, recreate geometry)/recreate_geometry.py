def recreate_geometry(vertices, start_nb):
    start_ver = vertices[start_nb]

    ver_1 = vertices[:start_nb]
    ver_1.append(start_ver) # closing polygon/ ostatni będą pierwszymi
    ver_2 = vertices[start_nb:-1]

    new_ver = ver_2 + ver_1
    geom = QgsGeometry.fromPolygonXY([new_ver])

    print(geom)
    return geom



mc = iface.mapCanvas()
poly_lyr = mc.currentLayer()

# find the corresponding (by name) point layer
all_lyrs = mc.layers()
poly_nm = poly_lyr.name()
point_lyr = None
for lyr in all_lyrs:
    point_nm = lyr.name()
    if point_nm[6:] == poly_nm:
        point_lyr = lyr
        



# creating memory layer
fn_out = "new_{}".format(os.path.basename(poly_lyr.source()))
lyr_out = QgsVectorLayer("Polygon", fn_out[:-4], "memory")
lyr_out.setCrs(poly_lyr.crs())

lyr_out.startEditing()
in_flds = poly_lyr.fields()
for fld in in_flds:
    lyr_out.addAttribute(fld)
lyr_out.commitChanges()

# recalculating geometry
start_coords = None

if point_lyr.isValid():
    for poly_ftr in poly_lyr.getFeatures():
        poly_geom = poly_ftr.geometry()
        poly_collect = poly_geom.asGeometryCollection()
        poly = poly_collect[0].asPolygon()
        poly_vertices = poly[0]

        request = QgsFeatureRequest()
        request.setFilterExpression("\"poly_id\" = {}".format(poly_ftr.id()))
        for point_ftr in point_lyr.getFeatures(request):
            ftr_id = point_ftr.id()
            
            point_geom = point_ftr.geometry()
            point_collect = point_geom.asGeometryCollection()
            
            start_coords =  point_collect[0].asPoint()
            start_x = start_coords.x()
            start_y = start_coords.y()
            
            new_geom = None
            for n, v in enumerate(poly_vertices):
                if v.x()==start_x and v.y()==start_y:
                    start_nb = n
                    new_geom = recreate_geometry(poly_vertices, start_nb)
            
            if new_geom:
                lyr_out.startEditing()
                ftr_out = QgsFeature(lyr_out.fields())
                ftr_out.setGeometry(new_geom)
                    
                # copying attributes from input layer to output
                in_flds = poly_lyr.fields()
                for fld in in_flds:
                   nm = fld.name()
                   idx = in_flds.indexOf(nm)
                   ftr_out.setAttribute(idx, ftr_in.attribute(nm))
               
                # adding created feature to output layer
                lyr_out.addFeature(ftr_out)
                # commiting changes
                lyr_out.commitChanges()
    # adding output layer to project
    QgsProject.instance().addMapLayer(lyr_out)

            
        