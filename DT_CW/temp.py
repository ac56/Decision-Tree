import numpy as np
import pandas as pd
import math


def find_potential_splits(current_df):
	previous_label = current_df.iloc[0,1]
	potential_splits = []
	for index, row in current_df.iterrows():
			if(previous_label != row['label']):
				previous_label = row['label']
				potential_splits.append(index)
	return potential_splits


def find_current_best_split(current_df):
	global label_list
	global labels_total
	
	potential_splits = find_potential_splits(current_df)
	best_split = potential_splits[0]
	best_entr_reduction = 0
	
	for current_split in potential_splits:
		split_entropy = 0
		temp_df = current_df.head(current_split)
		split_total_labels = len(temp_df.index)
		for label in label_list:
			count = temp_df['label'].value_counts().loc[label]
			split_entropy = split_entropy - (count/split_total_labels)* math.log2((count/split_total_labels))
		
		entropy_reduction =  (len(temp_df)/ labels_total) * split_entropy
		if (entropy_reduction > best_entr_reduction):
			best_entr_reduction = entropy_reduction
			best_split = current_split	
	return best_split, best_entr_reduction


def find_split(train_df):
	global label
	global all_labels
	best_entr_reduction = 0
	best_split	= {'attr': None, 'value': 0, 'index': 0}
#	all_labels = train_df[label].tolist()
	for i in train_df.columns:
		if(i == label ):
			continue

		all_val = train_df[i].tolist()
		
		current_df = pd.DataFrame(list(zip(all_val, all_labels)), 
							   columns =['wifi_strength', 'label'])
		
		current_df.sort_values(by=['wifi_strength'], ascending = True , inplace = True)
		current_df.reset_index(drop = True, inplace = True )		
		current_best_split, entropy_reduction = find_current_best_split(current_df)
		
		if (entropy_reduction > best_entr_reduction):
			best_entr_reduction = entropy_reduction
			best_split['attr'] = i
			best_split['value'] = current_df['wifi_strength'].iloc[current_best_split]
			best_split['index'] = current_best_split
	return best_split
		
def decision_tree_learning(train_df, depth):
	if(train_df.loc[:,'room'].var()==0):
		return ({'attr' : 'room' , 'value' : train_df[0, 'room'], 'left' : None, 'right' : None, 'leaf' : True }, depth)
	else:
		l_branch, r_branch = {}
		l_depth, r_depth = 0
		l_dataset, r_dataset = {} ################## dataframes to be assigned
		
		split = find_split (train_df)
		temp_df = train_df.sort_values(by=[split['attr']], ascending = True , inplace = True)
		temp_df.reset_index(drop = True, inplace = True )	
		left_df = current_df.head(current_split)
		
		node = {'attr' : split['attr'] , 'value' : split['value'], 'left' : None, 'right' : None, 'leaf' : False }
		l_branch, l_depth = decision_tree_learning(l_dataset, depth + 1)
		r_branch, r_depth = decision_tree_learning(r_dataset, depth + 1)
		return (node, max(l_depth, r_depth))
	
 
#################################################################################  MAIN  ############################################################################

clean_array = np.loadtxt('clean_dataset.txt')
attr_list = ['wifi1', 'wifi2', 'wifi3','wifi4', 'wifi5', 'wifi6', 'wifi7', 'room']
label = 'room'
train_df = pd.DataFrame(clean_array, columns = attr_list)
all_labels = train_df[label].tolist()
labels_total = len(all_labels)
label_list = set(all_labels)


################################################################################# TESTING ############################################################################



all_labels = train_df['room'].tolist()
print(train_df.columns)
all_val = train_df['wifi1'].tolist() 
#print(label_list)
#print(attr_list)
current_df = pd.DataFrame(list(zip(all_val, all_labels)), 
							   columns =['wifi_strength', 'label'])
current_df.sort_values(by=['wifi_strength'], ascending = True , inplace = True)
current_df.reset_index(drop = True, inplace = True)

potential_splits = find_potential_splits (current_df)
		
#print(current_df)
current_split = 200
		
temp_df = current_df.head(current_split)
split_total_labels = len(temp_df.index)
print(split_total_labels)
label = 1.0
print(temp_df)
#count = temp_df['label'].value_counts().loc[label]
temp2 = current_df['wifi_strength'].iloc[10]
print('temp2:')
print(temp2)
#print(count)
#split_total_labels = len(temp_df.index)
#print('total number of labels in temp_df :')
#print(split_total_labels)
#split_entropy = -(count/split_total_labels)* math.log2((count/split_total_labels))
#print (split_entropy)
#entropy_reduction =  (len(temp_df)/ labels_total) * split_entropy
#print ( (len(temp_df)/ labels_total))
#print('entropy reduction')
#print(entropy_reduction)
#print(temp_df)

######################################################################################################################################################################