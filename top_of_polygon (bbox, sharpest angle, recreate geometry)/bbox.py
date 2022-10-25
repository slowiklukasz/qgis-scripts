import os

mc = iface.mapCanvas()
lyrs = mc.layers()


for lyr_in in lyrs:
    if isinstance(lyr_in, QgsVectorLayer) and lyr_in.name()[:4] != "bbox":
        # creating output layer & setting right crs
        fn_out = "bbox_{}".format(os.path.basename(lyr_in.source()))
        lyr_out = QgsVectorLayer("Polygon", fn_out, "memory")
        lyr_out.setCrs(lyr_in.crs())
        
        # copying fields from input layer & creating field for bbox length
        lyr_out.startEditing()
        for fld in lyr_in.fields():
            lyr_out.addAttribute(fld)
        fld_len = QgsField("bbox_len", QVariant.Double, len=10, prec=2)
        lyr_out.addAttribute(fld_len)
        
        
        for ftr_in in lyr_in.getFeatures():
            geom = ftr_in.geometry()
            bbox_geom = geom.orientedMinimumBoundingBox()[0]
            bbox_area = geom.orientedMinimumBoundingBox()[1]
            bbox_angle = geom.orientedMinimumBoundingBox()[2]
            bbox_width = geom.orientedMinimumBoundingBox()[3]
            bbox_height = geom.orientedMinimumBoundingBox()[4]
            bbox_len = round(bbox_width) if bbox_width>bbox_height else round(bbox_height)
            
            if bbox_geom:
                # settign geometry to output feature
                rect = QgsRectangle.fromWkt(bbox_geom.asWkt())
                bbox_ftr = QgsFeature(lyr_out.fields())
                bbox_ftr.setGeometry(bbox_geom)

                # copying attributes from input layer to output
                flds = lyr_in.fields()
                for fld in flds:
                   nm = fld.name()
                   idx = flds.indexOf(nm)
                   bbox_ftr.setAttribute(idx, ftr_in.attribute(nm))
                   
                # creating new attributes
                fld_len = lyr_out.fields().indexOf("bbox_len")
                fld_width = lyr_out.fields().indexOf("bbox_width")
                fld_height = lyr_out.fields().indexOf("bbox_heigh")
                
                bbox_ftr.setAttribute(fld_len, bbox_len)
                bbox_ftr.setAttribute(fld_width, round(bbox_width))
                bbox_ftr.setAttribute(fld_height, round(bbox_height))
                
                # adding created feature to output layer
                lyr_out.addFeature(bbox_ftr)
                
        # commiting changes
        lyr_out.commitChanges()
        
        # setting proper style
        fn_style = r"C:\Users\lukas\Desktop\SKRYPTY\BBOX&LENGTH\style\bbox_style.qml"
        lyr_out.loadNamedStyle(fn_style)
        
        # adding output layer to project
        QgsProject.instance().addMapLayer(lyr_out)
    