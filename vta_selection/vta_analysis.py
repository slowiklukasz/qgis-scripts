import datetime as dt
import time

"""
**********************************************************************
SCRIPT TO SELECT THE NEWEST VTA FOR TREES WITH MORE THAN ONE VTA MADE.
ADDITIONALLY IT IS POSSIBLE TO MARK VTA FOR TREES WITH ONLY 1 VTA MADE
AND ALSO SELECT VTA BY RISK CLASS.
**********************************************************************
"""

"""USER INUTS"""
analyzed_layer = "vta" # layer to make selection (csv, xlsx, shp)

duplicated = True
non_duplicated = False

cat_a = True
cat_b = True
cat_c = True
cat_cd = True
cat_d = True


"""DONT TOUCH THIS PART!!!"""  
def select_duplicated_ftrs(ftrs):
    """Creates a list with features with multipled "ID Obiektu" field 
    value - some trees can have more than 1 VTA made."""

    # SELECTING VTA BY NEWEST DATE
    # list with "ID Obiektu" field for features with unique "ID Obiektu"
    single_ftrs = []

    # list with ids and "ID Obiektu" fields for features with repeated "ID Obiektu"
    duplicated_ftrs = []

    for ftr in ftrs:
        if ftr["ID Obiektu"] not in single_ftrs:
            single_ftrs.append(ftr["ID Obiektu"])
        else:
            if ftr["ID Obiektu"] not in duplicated_ftrs:
                duplicated_ftrs.append(ftr["ID Obiektu"])
                
    return duplicated_ftrs
    
    
def choose_newest_date(duplicated_ftrs):
    """Selecting ids of features with duplicated "ID Obiektu".
    Goal is to catch VTA with the newest date!!!"""
    
    duplicated_ids = []
    for oid in duplicated_ftrs:
        request = QgsFeatureRequest()
        request.setFilterExpression("\"ID Obiektu\" ={}".format(oid))
        
        date_lst = []
        tmp_ids = []
        
        for ftr in vta_lyr.getFeatures(request):
            tmp_date = ftr["Data realizacji"]
            
            date = dt.datetime.strptime(tmp_date, '%d/%m/%Y %H:%M:%S')
            date_lst.append(date)
            
            if date == max(date_lst):
                tmp_ids.clear()
                tmp_ids.append(ftr.id())
                
        duplicated_ids.append(tmp_ids[0])
    
    return duplicated_ids


def create_nonduplicated_lst(ftrs, duplicated_ftrs):
    """Creates a list with id for trees with only 1 VTA"""
    nonduplicated_ids = []
    for ftr in ftrs:
        if ftr["ID Obiektu"] not in duplicated_ftrs:
            nonduplicated_ids.append(ftr.id())
    return nonduplicated_ids
    

def rep_based_select(duplicated, non_duplicated):
    """Create list with duplicted (or not) "ID Obiektu" field"""
    selected_ids = []
    if duplicated==True and non_duplicated==True:
        selected_ids = duplicated_ids + nonduplicated_ids
    elif duplicated==False and non_duplicated==True:
        selected_ids = nonduplicated_ids
    elif duplicated==True and non_duplicated==False:
        selected_ids = duplicated_ids
    else:
        selected_ids = []
        
    return selected_ids


def risk_based_select(cat_a, cat_b, cat_c, cat_cd, cat_d, vta_lyr):
    """Creates list with ids of features that are not required in 
    selection because of risk class. Elements from this list will 
    be removed later using remove_redundand_ids function
    """
    expression = ""
    if not cat_a:
        expression += "or \"Klasa ryzyka\" like \'A%\'"
    if not cat_b:
        expression += "or \"Klasa ryzyka\" like \'B%\'"
    if not cat_c:
        expression += "or \"Klasa ryzyka\" like \'C %\'"
    if not cat_cd:
        expression += "or \"Klasa ryzyka\" like \'C-D%\'"
    if not cat_d:
        expression += "or \"Klasa ryzyka\" like \'D%\'"
    expression = expression[2:]
    
    ids_to_remove = []
    
    if expression != "":
        request = QgsFeatureRequest()
        request.setFilterExpression(expression)
        for ftr in vta_lyr.getFeatures(request):
            ids_to_remove.append(ftr.id())

    return ids_to_remove
    
    
def remove_redundand_ids(ids_lst, redundand_lst):
    """Removes redundand ids from ids used to select features"""
    diff_lst = []
    for i in ids_lst:
        if i not in redundand_lst:
            diff_lst.append(i)
            
    return diff_lst
    
    
if __name__ == "__console__":
    start = time.time()
    
    # OPENING LAYER, READ FEATURES
    vta_lyr = QgsProject.instance().mapLayersByName("{}".format(analyzed_layer))[0]
    ftrs = vta_lyr.getFeatures()
    
    # CREATE LIST WITH DUPLICATED "ID Obiektu" FIELD VALUE
    duplicated_ftrs = select_duplicated_ftrs(ftrs)
    
    # SELECTING VTA BY NEWEST DATE
    duplicated_ids = choose_newest_date(duplicated_ftrs)
    
    # LIST WITH IDS FOR FEATURES WITH NOT DUPLICTED "ID Obiektu"
    nonduplicated_ids = create_nonduplicated_lst(ftrs, duplicated_ftrs)

    # SELECTION BASED ON REPETITION OF "ID Obiektu" FIELD
    selected_ids = rep_based_select(duplicated, non_duplicated)
    
    # SELECTION BASED ON CLASS RISK
    red_lst = risk_based_select(cat_a, cat_b, cat_c, cat_cd, cat_d, vta_lyr)
    final_lst = remove_redundand_ids(selected_ids, red_lst)

    # FINALL CALCULATION
    vta_lyr.removeSelection()
    vta_lyr.selectByIds(final_lst)
    
    stop = time.time()
    print("Finished in: {} seconds".format(round(stop-start, 2)))
    print("Number of selected features: {}".format(vta_lyr.selectedFeatureCount()))