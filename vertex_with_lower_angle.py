from math import degrees


def calc_angle(v_1, v_2, v_3):
    """
    Calculating the angle between the 3 selected vertices.
    """
    # https://gis.stackexchange.com/questions/380320/finding-interior-angles-of-a-triangle-using-pyqgis      
    triangle = QgsTriangle(v_1, v_2, v_3)
    angles = [round(degrees(a), 2) for a in triangle.angles()]
        
    return angles
    
    
def create_angles_lst(vertices_lst, idx_lst):
    """
    Creating a list with all polygon angles.
    In: 1) list of QgsPointXY from polygon,
        2) list of indices of verticles placed on shorter side of bbox
    Out: list with selected angles inside of polygon
    """
    
    angls_lst = []
    n = len(vertices_lst)
    for i in range(n-1): # last angle == first angle
        if i==0:
            v_1 = vertices_lst[-2] # lst[-1] == lst[0] -> QgsPolygon
        else:
            v_1 = vertices_lst[i-1] # lst[-1] == lst[0] -> QgsPolygon
        v_2 = vertices_lst[i]
        v_3 = vertices_lst[i+1]
        angl = calc_angle(v_1, v_2, v_3)
        angls_lst.append(angl[1])
    
    angls_lst.append(angls_lst[0]) # [-1] == [0] -> QgsPolygon
    angls_lst = [a for i, a in enumerate(angls_lst) if i in idx_lst]  
    
    return angls_lst
    

def bbox_shorter_sides(vertices_lst):
    """
    Selection of shorter sides of bbox.
    In: list of QgsPointXY from bbox
    Out: returns 2 line geometries)
    """
    v1, v2, v3, v4, v1 = vertices_lst
    
    l1 = QgsGeometry.fromPolylineXY([v1, v2])
    l2 = QgsGeometry.fromPolylineXY([v2, v3])
    l3 = QgsGeometry.fromPolylineXY([v3, v4])
    l4 = QgsGeometry.fromPolylineXY([v4, v1])
    
    l1_len = l1.length()
    l2_len = l2.length()
    l3_len = l3.length()
    l4_len = l4.length()
    
    shrt_sd1, shrt_sd2 = (l1, l3) if l1_len < l2_len else (l2, l4)
    
    return (shrt_sd1, shrt_sd2)


def vertices_on_bbox(poly_vertices, side_1, side_2):
    """
    Selection of vertices placed on the shorter side of bbox.
    In: 1) list of QgsPointXY from polygon, 
        2) 1st geometry of shorter bbox side,
        3) 2nd geometry of shorter bbox side.
    Out:1) List with the indices of the vertices placed on the shorter sides of the bbox
        2) List with the  vertices placed on the shorter sides of the bbox
    """
    idx_lst = []
    vtx_lst = []
    for i, v in enumerate(poly_vertices):
        v_geom = QgsGeometry.fromPointXY(v).buffer(0.00001,8)
        if side_1.crosses(v_geom) or side_2.crosses(v_geom): 
            if v not in vtx_lst:
                idx_lst.append(i)
                vtx_lst.append(v)
    
    return idx_lst, vtx_lst


def sharpest_vertex(angls_lst, vtx_lst):
    """ Selecting the vertex with the sharpest angle.
    In: 1) List of vertices placed on shorter side of bbox
        2) List with the vertices placed on the shorter sides of the bbox
    Out: Vertex with the sharpest angle
    """

    angl_min = max(angls_lst) +1
    
    for v, a in zip(vtx_lst, angls_lst):
        if a < angl_min:
            angl_min = a
            vertex_min = v
#    print("Min. angle: {},x: {}, y: {}".format(angl_min,vertex_min.x(), vertex_min.y()))
    
    return vertex_min



if __name__ == "__console__":
    # layer selection
    mc = iface.mapCanvas()
    lyr_in = mc.currentLayer()

    # A. CREATING MEMORY LAYER
    fn_out = "top_v_{}".format(os.path.basename(lyr_in.source()))
    lyr_out = QgsVectorLayer("Point", fn_out, "memory")
    lyr_out.setCrs(lyr_in.crs())
    
    lyr_out.startEditing()
    fld_x = QgsField("x_coord", QVariant.Double, len=50, prec=10)
    fld_y = QgsField("y_coord", QVariant.Double, len=50, prec=10)
    lyr_out.addAttribute(fld_x)
    lyr_out.addAttribute(fld_y)
    
    for ftr_in in lyr_in.getFeatures():
        # B. SEARCHING FOR VERTEX WITH MINIMUM ANGLE
        geom = ftr_in.geometry()
        bbox_geom = geom.orientedMinimumBoundingBox()[0]
        
        poly = geom.asGeometryCollection()
        bbox_poly = geom.asGeometryCollection()

        poly_vertices = poly[0].asPolygon()[0]
        bbox_vertices = bbox_geom.asPolygon()[0] # bbox_poly[0].asPolygon()[0]
        
        side_1, side_2 = bbox_shorter_sides(bbox_vertices)
        idx_lst, vtx_lst = vertices_on_bbox(poly_vertices, side_1, side_2)
    
        angls_lst = create_angles_lst(poly_vertices, idx_lst)
        vtx_start = sharpest_vertex(angls_lst, vtx_lst)
        
        # C. CREATING ADDING FEATURE TO THE OUTPUT LAYER
        # creating output feature
        ftr_out = QgsFeature(lyr_out.fields())
        
        # setting geometry to output feature
        geom = QgsGeometry.fromPointXY(vtx_start)
        ftr_out.setGeometry(geom)
        
        # creating x_coord, y_coord attributes
        fld_x_idx = lyr_out.fields().indexOf("x_coord")
        fld_y_idx = lyr_out.fields().indexOf("y_coord")
        
        ftr_out.setAttribute(fld_x_idx, vtx_start.x())
        ftr_out.setAttribute(fld_y_idx, vtx_start.y())
        
        # adding output feature to the output layer
        lyr_out.addFeature(ftr_out)
        
    # commiting changes
    lyr_out.commitChanges()

    # setting proper style
    fn_style = r"sharpest_vertex.qml"
    lyr_out.loadNamedStyle(fn_style)
    
    # adding output layer to project
    QgsProject.instance().addMapLayer(lyr_out)
