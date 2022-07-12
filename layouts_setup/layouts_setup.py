from qgis.PyQt import  QtGui
project = QgsProject.instance()

# LAYER TO PRINT
layer_to_print = 'P1'

# PAGE FORMATING
format = 'A4'
orientation = None # Portrait or Landscape
margin = 2.5
scale = 1.3

# LEGEND FORMATING
legend_orientation = 'Landscape' # Portrait or Landscape
legend_margin = 4
columns = 1

def changing_lyrs_names():
    lyrs_lst = ['P1', 'P2', 'L1', 'L2', 'S1', 'S2', 'S3']

    if lyrs_lst !=[]:
        for layer in iface.mapCanvas().layers():
            for i in lyrs_lst:
                if layer.name().startswith(i):
                    layer.setName(i)

def create_lyt_view(lyt_name, page_format, lyr_to_extent, orientation=None): 
    # create layout view
    project = QgsProject.instance()
    manager = project.layoutManager()
    layoutName = lyt_name
    layouts_list = manager.printLayouts()

    # remove duplitated layouts
    for layout in layouts_list:
        if layout.name() == layoutName:
            manager.removeLayout(layout)
    
    # adding layout to the project
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layoutName)
    
    # setting map to layer extent
    pc = layout.pageCollection()
    if orientation=='Portrait':
        pc.pages()[0].setPageSize(page_format, QgsLayoutItemPage.Orientation.Portrait)
    elif orientation=='Landscape':
        pc.pages()[0].setPageSize(page_format, QgsLayoutItemPage.Orientation.Landscape)
    elif not orientation:
        if lyr_to_extent:
            if lyr_to_extent.extent().width() >= lyr_to_extent.extent().height():
                pc.pages()[0].setPageSize(page_format, QgsLayoutItemPage.Orientation.Landscape)
            else:
                pc.pages()[0].setPageSize(page_format, QgsLayoutItemPage.Orientation.Portrait)
    manager.addLayout(layout)
    
    return layout


def create_map_item(layout, lyr_to_extent, margin=0, scale=1.5):
    # adding map item to the layout
    map = QgsLayoutItemMap(layout)
    map.setRect(1,1,1,1)
    
    # setting layer extent
    ms = QgsMapSettings()
    ms.setLayers([layer])
    rect = QgsRectangle(ms.fullExtent())
    rect.scale(scale)
    ms.setExtent(rect)
    map.setExtent(rect)
    layout.addLayoutItem(map)

    # setting layout size
    map.attemptMove(QgsLayoutPoint(margin, margin, QgsUnitTypes.LayoutMillimeters))
    pc = layout.pageCollection()
    h = pc.pages()[0].pageSize().height()
    w = pc.pages()[0].pageSize().width()
    
    map.attemptResize(QgsLayoutSize(w - margin*2, h - margin*2, QgsUnitTypes.LayoutMillimeters))
    map.attemptMove(QgsLayoutPoint(margin, margin, QgsUnitTypes.LayoutMillimeters))
    
    # adding layout frame
    map.setFrameEnabled(True)
    map.zoomToExtent(rect)
    
    return map


def read_group_name(layer):
    root = QgsProject.instance().layerTreeRoot()
    tree_layer = root.findLayer(layer.id())
    if tree_layer:
        layer_parent = tree_layer.parent()
        
    return layer_parent, layer_parent.name()


def create_map_legend(layout, layout_name, project, legend_orientation=None, legend_margin=0, columns=None):
    legend = QgsLayoutItemLegend(layout)
    legend.setTitle("Legenda - {}".format(layout_name))
    layerTree = QgsLayerTree()

    names_lst = []
    for lyr in iface.mapCanvas().layers():
        if lyr.name() not in names_lst:
            names_lst.append(lyr.name())
            if isinstance(lyr, QgsVectorLayer):
                if QgsProject.instance().layerTreeRoot().findLayer(lyr.id()).isVisible:
                    layerTree.addLayer(lyr)
                    layerTree.setParent(lyr.parent())

    legend.model().setRootGroup(layerTree)
    legend.setFrameEnabled(True)
    layout.addLayoutItem(legend)
    legend.setLegendFilterByMapEnabled(True)

    # setting margins
    projectLayoutManager = project.layoutManager()
    layout = projectLayoutManager.layoutByName(layout_name)
    legend = layout.itemById(legend.id())
    legend.attemptMove(QgsLayoutPoint(2.5,2.5, QgsUnitTypes.LayoutMillimeters))

    # https://api.qgis.org/api/classQgsLayoutItemLegend.html#ac1842f95a9652810af008e1b3fc8d4ba
    legend.setStyleFont(QgsLegendStyle.Title, QFont("Yu Gothic", 15, QFont.Bold))
    legend.setStyleFont(QgsLegendStyle.Group, QFont("Yu Gothic", 7, QFont.Bold))
    legend.setStyleFont(QgsLegendStyle.Subgroup, QFont("Yu Gothic", 7, QFont.Bold))
    legend.setStyleFont(QgsLegendStyle.SymbolLabel, QFont("Yu Gothic", 4))
    
    legend.rstyle(QgsLegendStyle.Title).setMargin(10)
    legend.rstyle(QgsLegendStyle.Group).setMargin(5)
    legend.rstyle(QgsLegendStyle.Subgroup).setMargin(5)
    
    legend.setSymbolHeight(1.5)
    legend.setSymbolWidth(1.5)
    legend.setColumnCount(1.5)
    legend.setColumnSpace(1)
    legend.setLineSpacing(10)
    
    legend.setAutoUpdateModel(True)
    legend.setSplitLayer(True)
    legend.updateFilterByMap(True)
#    legend.adjustBoxSize()
    legend.setSplitLayer(True)
    legend.equalColumnWidth()
    
    if columns:
        legend.setColumnCount(columns)
    else:
        if legend_orientation == 'Landscape':
            legend.setColumnCount(6)
        else:
            legend.setColumnCount(3)
    legend.legendFilterByMapEnabled()
    legend.refresh()


if __name__ == '__console__':
    # create layout for each layer with  specific name
    ids = []
    changing_lyrs_names()
    
    for layer in iface.mapCanvas().layers():
        if layer.name() == layer_to_print:
            ids.append(layer.id())
    
    if ids == []:
        print('No layer selected!')
    else:
        for layer in iface.mapCanvas().layers():
            for lyr_id in ids:
                if layer.id() == lyr_id:
                    layout_name = read_group_name(layer)[1]
                    layout = create_lyt_view(layout_name, format, layer, orientation)
                    create_map_item(layout, layer, margin, scale)
                    create_map_legend(layout, layout_name, project, legend_orientation, legend_margin, columns)
#                    iface.openLayoutDesigner(layout)
                    print('Layout \'{}\' has been created. You can open it using layout manager and apply some additional setups'.format(layout_name))
                    print()
#                QgsProject.instance().layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(False)
    iface.showLayoutManager ()
