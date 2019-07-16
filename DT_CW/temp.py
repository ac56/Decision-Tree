import numpy as np
import pandas as pd


def find_split(train_df):
	df['one'].tolist()
	pass
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


print(train_df.loc[:,'room'].var())

#print(len(set(train_df['room'])))


#print(clean_array)

print("hello")













