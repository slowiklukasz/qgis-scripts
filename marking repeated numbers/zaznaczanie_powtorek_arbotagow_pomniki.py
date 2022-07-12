''' WYSZUKIWANIE POWTARZAJĄCYCH SIĘ ARBOTAGÓW'''
layer = iface.activeLayer()
features=layer.getFeatures()

selected_fid=[]
tag_list=[]

for feature in features:
    attrs = feature.attributes()
    arbotag=attrs[1]
    tag_list.append((arbotag,feature.id()))


rpt_list=[]
ind_list=[]
for tag,ind in tag_list:
    if tag not in rpt_list:
        rpt_list.append(tag)
        ind_list.append(ind)
        
layer.select(ind_list)
layer.invertSelection()

print('done')