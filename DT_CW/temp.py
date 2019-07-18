import numpy as np
import pandas as pd
import math
import time

def find_potential_splits(current_df):
	previous_label = current_df.iloc[0,1]
	potential_splits = []
	for index, row in current_df.iterrows():
			if(previous_label != row['label']):
				previous_label = row['label']
				potential_splits.append(index)
	return potential_splits


def find_current_best_split(current_df):
	global labels_total
	global label
	
	potential_splits = find_potential_splits(current_df)
	best_split = potential_splits[0]
	best_entr_reduction = 0
	
	

	for current_split in potential_splits:
		split_entropy = 0
		temp_df = current_df.head(current_split)
		split_total_labels = len(temp_df.index)
		label_list = set(temp_df['label'])
		# print(label_list)
		# print(temp_df)
		for current_label in label_list:
			count = temp_df['label'].value_counts().loc[current_label]
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
		#print(i)
		if(i == label ):
			continue

		all_val = train_df[i].tolist()
		
		current_df = pd.DataFrame(list(zip(all_val, all_labels)), 
							   columns =['attr_value', 'label'])
		
		current_df.sort_values(by=['attr_value'], ascending = True , inplace = True)
		current_df.reset_index(drop = True, inplace = True )		
		current_best_split, entropy_reduction = find_current_best_split(current_df)
		
		if (entropy_reduction > best_entr_reduction):
			best_entr_reduction = entropy_reduction
			best_split['attr'] = i
			best_split['value'] = current_df['attr_value'].iloc[current_best_split]
			best_split['index'] = current_best_split
	return best_split
		
def decision_tree_learning(train_df, depth):
	if(train_df.loc[:,'room'].var()==0):
		return ({'attr' : 'room' , 'value' : train_df[0, 'room'], 'left' : None, 'right' : None, 'leaf' : True }, depth)
	else:

		
		split = find_split (train_df)
		
		# print('split found')
		virtual_node = {'attr' : split['attr'] , 'value' : split['value'], 'left' : 'TBD', 'right' : 'TBD', 'depth' : depth, 'leaf' : False }
		time_stamp = time.time() - start
		print(virtual_node)
		print('time elapsed:')
		print(time_stamp)
		print('\n')
		

		temp_df = train_df.sort_values(by=[split['attr']], ascending = True )
		temp_df.reset_index(drop = True, inplace = True )	

		print('split at index:')
		print(split['index'])
		l_dataset = temp_df.iloc[ : split['index'], :]
		l_rows = len(l_dataset[split['attr']])
		# l_dataset = l_dataset.drop(split['attr'])
		
		r_dataset = temp_df.iloc[split['index']:, :]
		r_rows = len(r_dataset[split['attr']])
		# r_dataset = r_dataset.drop(split['attr'])
		print('rows in left dataset:')
		print(l_rows)
		print('rows in right dataset:')
		print(r_rows)
		
		l_branch, l_depth = decision_tree_learning(l_dataset, depth + 1)
		r_branch, r_depth = decision_tree_learning(r_dataset, depth + 1)
		
		node = {'attr' : split['attr'] , 'value' : split['value'], 'left' : l_branch, 'right' : r_branch, 'depth':depth, 'leaf' : False }
		return (node, max(l_depth, r_depth))
	
 
#################################################################################  MAIN  ############################################################################
start = time.time()
print ("hello")
clean_array = np.loadtxt('clean_dataset.txt')
attr_list = ['wifi1', 'wifi2', 'wifi3','wifi4', 'wifi5', 'wifi6', 'wifi7', 'room']
label = 'room'
train_df = pd.DataFrame(clean_array, columns = attr_list)
all_labels = train_df[label].tolist()
labels_total = len(all_labels)

depth = 0

tree = decision_tree_learning(train_df, depth)

print(tree)
################################################################################# TESTING ############################################################################



# all_labels = train_df['room'].tolist()
# print(train_df.columns)
# all_val = train_df['wifi1'].tolist() 
# #print(label_list)
# #print(attr_list)
# current_df = pd.DataFrame(list(zip(all_val, all_labels)), 
# 							   columns =['attr_value', 'label'])
# current_df.sort_values(by=['attr_value'], ascending = True , inplace = True)
# current_df.reset_index(drop = True, inplace = True)

# potential_splits = find_potential_splits (current_df)
		
# #print(current_df)
# current_split = 200
# #count = temp_df['label'].value_counts().loc[label]
# best_split = {}
# best_split['attr'] = 'wifi1'
# best_split['value'] = current_df['attr_value'].iloc[current_split]
# best_split['index'] = current_split
# print(best_split)
# split_point = best_split['index']
# print(split_point)

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