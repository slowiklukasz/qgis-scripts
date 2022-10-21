
from math import degrees
import itertools


def calc_angle(v_1, v_2, v_3):
    # https://gis.stackexchange.com/questions/380320/finding-interior-angles-of-a-triangle-using-pyqgis
    # points = [QgsPointXY(0, 0), QgsPointXY(1, 2), QgsPointXY(2, 0)]
    points = [v_1, v_2, v_3]
    n = len(points)
    per = range(n)

    for i, j, k in itertools.permutations(per, 3):
        triangle = QgsTriangle( points[i], points[j], points[k])
        angles = [round(degrees(a), 2) for a in triangle.angles()]
        
    return angles
    
    
def create_angles_lst(vertiles_lst):
    angls_lst = []
    n = len(vertiles_lst)
    for i in range(n-1): # last angle == first angle
        if i==0:
            v_1 = vertiles_lst[-2] # [-1] == [0] -> QgsPolygon
            v_2 = vertiles_lst[i]
            v_3 = vertiles_lst[i+1]
            angl = calc_angle(v_1, v_2, v_3)
            angls_lst.append(angl[1])
            print(angl[1])
        else:
            v_1 = vertiles_lst[i-1] # [-1] == [0] -> QgsPolygon
            v_2 = vertiles_lst[i]
            v_3 = vertiles_lst[i+1]
            angl = calc_angle(v_1, v_2, v_3)
            angls_lst.append(angl[1])
            print(angl[1])
            
    angls_lst.append(angls_lst[0]) # [-1] == [0] -> QgsPolygon
    
    return angls_lst


if __name__ == "__console__":
    # layer selection
    mc = iface.mapCanvas()
    lyrs = mc.layers()
    lyr = lyrs[0]
    ftrs = lyr.selectedFeatures()
    ftr = ftrs[0]

    geom = ftr.geometry()
    poly = geom.asGeometryCollection()
    # poly[0] - 1st element of list
    # poly[0].asPolygon()[0] - 2st list with points
    vertiles_lst = poly[0].asPolygon()[0]
    
    angls_lst = create_angles_lst(vertiles_lst)

    angl_min = max(angls_lst) +1
    for v, a in zip(vertiles_lst, angls_lst):
        if a < angl_min:
            angl_min = a
            vertex_min = v
            
    print(angl_min)

    cntr = QgsPointXY(  vertex_min.x(), vertex_min.y())
    mc.setCenter(cntr)
    mc.zoomScale(100)


