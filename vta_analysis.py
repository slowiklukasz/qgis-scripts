import datetime

# Get input (xls) and target (Shapefile) layers
vta_lyr = QgsProject.instance().mapLayersByName("vta")[0]
#print(vta_lyr.attributeAliases())

ftrs = vta_lyr.getFeatures()
#print("featuresCount: {}".format(vta_lyr.featureCount())) # 20835

ids_lst = [] # id with unique "ID Obiektu" in list
ftrs_lst = [] # objects with repeated "ID Obiektu" in list

duplicated_ids = []
duplicated_ftrs = []

i = 0
for ftr in ftrs:
    i+=1
    if i >1400:
        break
    
    if ftr["ID Obiektu"] not in ftrs_lst:
        ids_lst.append(ftr.id())
        ftrs_lst.append(ftr["ID Obiektu"])
    else:
        duplicated_ids.append(ftr.id())
        
        if ftr["ID Obiektu"] not in duplicated_ftrs:
            duplicated_ftrs.append(ftr["ID Obiektu"])


secnd_ids = []

for oid in duplicated_ftrs:
    request = QgsFeatureRequest()
    request.setFilterExpression("\"ID Obiektu\" ={}".format(oid))
    
    date_lst = []
    tmp_ids = []
    
    for ftr in vta_lyr.getFeatures(request):
        tmp_date = ftr["Data realizacji"]
        
        date = datetime.datetime.strptime(tmp_date, '%d/%m/%Y %H:%M:%S')
        date_lst.append(date)
        if date == max(date_lst):

            tmp_ids.clear()
            tmp_ids.append(ftr.id())
            
    secnd_ids.append(tmp_ids[0])
        
print("secnd_ids: {}".format(secnd_ids))

first_ids = []
for ftr in ftrs:
    if ftr["ID Obiektu"] not in duplicated_ftrs:
            first_ids.append(ftr["ID Obiektu"])
            
chk_lst = []
for i in first_ids:
    if i in secnd_ids:
        chk_lst.append(i)
        
print("cjck_lst: {}".format(chk_lst))



        


