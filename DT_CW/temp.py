import numpy as np
import pandas as pd


def find_split(train_df):
	label_list = train_df["room"].tolist()
	for i in range(len(train_df.columns)-1):
		entropy = 0
		previous_label = label_list[0]
		attr_list = train_df[i].tolist()
		
		current_df = pd.DataFrame(list(zip(attr_list, label_list)), 
							   columns =['wifi_strength', 'label'])
		
		current_df.sort_values(by=['wifi_strength'], ascending = True , inplace = True)
		current_df.reset_index( inplace = True )
		previous_value = current_df #*****************************************assign first wifi strength
		potential_splits = []
		
		
		for index, row in current_df.iterrows():
			if(previous_label != row['label']):
				previous_label = row['label']
				potential_splits.append()
		
			
		
#	
	
def decision_tree_learning(train_df, depth):
	if(train_df.loc[:,'room'].var()==0):
		return ({"attr" : "room" , "value" : train_df[0, "room"], "left" : None, "right" : None, "leaf" : True }, depth)
	else:
		l_branch, r_branch = {}
		l_depth, r_depth = 0
		l_dataset, r_dataset = {}
		
		split = find_split (train_df)
		node = {"attr" : split["attr"] , "value" : split["value"], "left" : None, "right" : None, "leaf" : False }
		l_branch, l_depth = decision_tree_learning(l_dataset, depth + 1)
		r_branch, r_depth = decision_tree_learning(r_dataset, depth + 1)
		return (node, max(l_depth, r_depth))
	
 


clean_array = np.loadtxt("clean_dataset.txt")
train_df = pd.DataFrame(clean_array, columns = ["wifi1", "wifi2", "wifi3","wifi4", "wifi5", "wifi6", "wifi7", "room" ])

print (len(train_df.columns))
print(train_df.loc[:,'room'].var())

label_list = train_df["room"].tolist()
attr_list = train_df['wifi1'].tolist()
#print(label_list)
#print(attr_list)
current_df = pd.DataFrame(list(zip(attr_list, label_list)), 
							   columns =['wifi_strength', 'label'])
current_df.sort_values(by=['wifi_strength'], ascending = True , inplace = True)









#
#print (current_df)
#for index, row in current_df.iterrows():
#	print(row['label'])



#print(len(set(train_df['room'])))


#print(clean_array)















