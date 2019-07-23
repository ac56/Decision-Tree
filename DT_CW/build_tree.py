import math
import setup
import pandas as pd

def find_potential_splits(current_df):
	previous_value = current_df.iloc[0,0]
	previous_label = current_df.iloc[0,1]
	potential_splits = []
	for index, row in current_df.iterrows():
			if((previous_label != row['label']) and (previous_value != current_df.iloc[index, 0])):
				previous_label = row['label']
				potential_splits.append(index)
			previous_value = current_df.iloc[index, 0]
			previous_label = row['label']
	return potential_splits
###########################################################################################################################################
def find_current_best_split(current_df):
	setup.label
	#print('Ready to enter find_potential_splits function...\n')
	potential_splits = find_potential_splits(current_df)
	#print('list of potential splits in current dataframe:')
	#print(potential_splits)
	#print('\n')
	if(not potential_splits):
		return (-1), (-1)
	else:
		best_split = potential_splits[0]
	least_curr_entropy = 0
	first = True
	for current_split in potential_splits:
		#print('split under consideration:')
		#print(current_split)
		curr_split_entropy = 0
		l_split_entr = 0
		r_split_entr = 0
		temp_left_df = current_df.iloc[:current_split, : ]
		temp_right_df = current_df.iloc[current_split:, : ]

		left_total_labels = len(temp_left_df.index)
		left_label_list = set(temp_left_df['label'])
		right_total_labels = len(temp_right_df.index)
		right_label_list = set(temp_right_df['label'])
		# print(left_label_list)
		# print(temp_left_df)
		for current_label in left_label_list:
			count = temp_left_df['label'].value_counts().loc[current_label]
			l_split_entr = l_split_entr - (count/left_total_labels)* math.log2((count/left_total_labels))
			#print('There are ' + str(count) + ' ' + str(current_label) + 's in the left temporary dataframe')
		#print('left split entropy is '+str(l_split_entr))
		#print(' (len(temp_left_df)/ len(current_df)) = ' +str( (len(temp_left_df)/ len(current_df))))
		curr_split_entropy =  (len(temp_left_df)/ len(current_df)) * l_split_entr
		#print('\n')
		for current_label in right_label_list:
			count = temp_right_df['label'].value_counts().loc[current_label]
			r_split_entr = r_split_entr - (count/right_total_labels)* math.log2((count/right_total_labels))
			#print('There are ' + str(count) + ' ' + str(current_label) + 's in the right temporary dataframe')
		#print('right split entropy is '+str(r_split_entr))
		#print(' (len(temp_right_df)/ len(current_df)) = ' +str( (len(temp_right_df)/ len(current_df))))
		curr_split_entropy +=  (len(temp_right_df)/ len(current_df)) * r_split_entr
		#print('*******************The TOTAL entropy of split ' + str(current_split) + ' is \t' + str(curr_split_entropy))
		# if ((curr_split_entropy < least_curr_entropy) and (first == False)):
		# 	least_curr_entropy = curr_split_entropy
		# 	best_split = current_split
		if (first == True):
			best_split = current_split
			least_curr_entropy = curr_split_entropy
			first = False
		else:
			if((curr_split_entropy < least_curr_entropy)):
				least_curr_entropy = curr_split_entropy
				best_split = current_split
		#print('*********Currently the best split for ' + current_df.columns[0] + ' is at position ' + str(best_split) + ' with an entropy of ' + str(least_curr_entropy) + '\n'	)
	return best_split, least_curr_entropy
###########################################################################################################################################
def find_split(train_df):
	setup.label
	#global all_labels
	least_curr_entropy = 0
	curr_split_entropy = 0
	first = True
	best_split	= {'attr': None, 'value': 0, 'index': 0}
	train_labels = train_df[setup.label].tolist()
	for i in train_df.columns:
		#print(i)
		if(i == setup.label ):
			continue
		all_val = train_df[i].tolist()
		current_df = pd.DataFrame(list(zip(all_val, train_labels)), 
							   columns =[i, 'label'])
		#print('current unsorted dataframe for column ' + i + ' is:')
		#print(current_df)
		current_df.sort_values(by=[i], ascending = True , inplace = True)
		current_df.reset_index(drop = True, inplace = True )
		#print('current sorted dataframe is:')
		#print(current_df)
		#print('Ready to enter find_current_best_split function...\n')		
		current_best_split, curr_split_entropy = find_current_best_split(current_df)
		if(current_best_split == -1):
			continue
		if ((curr_split_entropy < least_curr_entropy) and (first == False)):
			least_curr_entropy = curr_split_entropy
			best_split['attr'] = i
			best_split['value'] = (current_df[i].iloc[current_best_split] + current_df[i].iloc[current_best_split - 1]) / 2
			best_split['index'] = current_best_split
		if(first):
			least_curr_entropy = curr_split_entropy
			best_split['attr'] = i
			best_split['value'] = (current_df[i].iloc[current_best_split] + current_df[i].iloc[current_best_split - 1]) / 2
			best_split['index'] = current_best_split
			first = False
		#print('\n')
	#print( 'The least entropy found is ' + str(least_curr_entropy) + ' on attribute ' + str(best_split['attr']) + '\n' )
	return best_split
###########################################################################################################################################		
def decision_tree_learning(train_df, depth):
	if((train_df[setup.label].nunique() == 1)):
		temp_list = train_df[setup.label]
		#print('temp_list:')
		#print(temp_list)
		return ({'attr' : setup.label , 'value' : temp_list[0], 'left' : None, 'right' : None, 'leaf' : True }, depth)
	else:
		split = find_split (train_df)
		if (split['attr'] == None):
			value = train_df[setup.label].value_counts().argmax()
			return ({'attr' : setup.label , 'value' : value, 'left' : None, 'right' : None, 'leaf' : True }, depth)
		# print('the following split is to take place:')
		# print(split)
		#decided_splits_list.append((str(split['attr']) + '>' + str(split['value'])))
		#print('\nDecided splits until now are:')
		#print(decided_splits_list)
		#print('\n')
		# print('split found')
		#virtual_node = {'attr' : split['attr'] , 'value' : split['value'], 'left' : 'TBD', 'right' : 'TBD', 'depth' : depth, 'leaf' : False }
		temp_df = train_df.sort_values(by=[split['attr']], ascending = True )
		temp_df.reset_index(drop = True, inplace = True )	
		#print('Sorted dataframe in respect to ' + str(split['attr'])+ ' :')
		#print(temp_df)
		#print('\n')
		#print('split at index:')
		#print(split['index'])
		l_dataset = temp_df.iloc[ : split['index'], :]
		#l_rows = len(l_dataset[split['attr']])
		# l_dataset = l_dataset.drop(split['attr'])
		r_dataset = temp_df.iloc[split['index']:, :]
		r_dataset.reset_index(drop = True, inplace = True)
		#r_rows = len(r_dataset[split['attr']])
		# r_dataset = r_dataset.drop(split['attr'])
		#print('rows in left dataset:')
		#print(l_rows)
		#print('rows in right dataset:')
		#print(r_rows)
		#print('\n' * 15)
		l_branch, l_depth = decision_tree_learning(l_dataset, depth + 1)
		r_branch, r_depth = decision_tree_learning(r_dataset, depth + 1)
		node = {'attr' : split['attr'] , 'value' : split['value'], 'left' : l_branch, 'right' : r_branch, 'leaf' : False }
		return (node, max(l_depth, r_depth))
#################################################################################  MAIN  ############################################################################
# start = time.time()
# print ("hello")
# clean_array = np.loadtxt('smaller_dataset.txt')
# attr_list = ['wifi1', 'wifi2', 'wifi3','wifi4', 'wifi5', 'wifi6', 'wifi7', 'room']
# label = 'room'
# train_df = pd.DataFrame(clean_array, columns = attr_list)

# # all_labels = train_df[label].tolist()
# # labels_total = len(all_labels)

# depth = 0

# decided_splits_list = []
# tree = decision_tree_learning(train_df, depth)

# print(tree)
################################################################################# TESTING ############################################################################
# all_labels = train_df['room'].tolist()
# print(train_df.columns)
# all_val = train_df['wifi1'].tolist() 
# #print(left_label_list)
# #print(attr_list)
# current_df = pd.DataFrame(list(zip(all_val, all_labels)), 
# 							   columns =[i, 'label'])
# current_df.sort_values(by=[i], ascending = True , inplace = True)
# current_df.reset_index(drop = True, inplace = True)

# potential_splits = find_potential_splits (current_df)
		
# #print(current_df)
# current_split = 200
# #count = temp_df['label'].value_counts().loc[label]
# best_split = {}
# best_split['attr'] = 'wifi1'
# best_split['value'] = current_df[i].iloc[current_split]
# best_split['index'] = current_split
# print(best_split)
# split_point = best_split['index']
# print(split_point)

#print(count)
#left_total_labels = len(temp_df.index)
#print('total number of labels in temp_df :')
#print(left_total_labels)
#split_entropy = -(count/left_total_labels)* math.log2((count/left_total_labels))
#print (split_entropy)
#curr__split_entropy =  (len(temp_df)/ labels_total) * split_entropy
#print ( (len(temp_df)/ labels_total))
#print('entropy reduction')
#print(curr__split_entropy)
#print(temp_df)
######################################################################################################################################################################