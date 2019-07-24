import setup
import pandas as pd
import build_tree
import predict
import assess


def prune_tree(tree_node, valid_set):
    valid_answers = valid_set[setup.label]
    valid_answers.reset_index(drop = True , inplace = True)
    valid_set = valid_set.drop([setup.label], axis = 1)

    prune_list = []
    prune_list = find_potential_prunes (tree_node, prune_list)

    valid_prediction_list = []
    for index, row in valid_set.iterrows():
        predicted_label = predict.predict_label ( tree_node, row)
        valid_prediction_list.append(predicted_label)
    previous_score = assess.set_score (valid_prediction_list, valid_answers)

    for prune in prune_list:
        
    return tree_node

def find_potential_prunes (tree_node, prune_list):
    #print('entered find_potential_prunes')
    if( tree_node['leaf'] == True):
        #print('alow')
        return prune_list
    else:
        if ( (tree_node['left']['leaf'] == True) and (tree_node['right']['leaf'] == True) ):
            prune_list.append(tree_node)
        prune_list = find_potential_prunes (tree_node['left'], prune_list)
        prune_list = find_potential_prunes (tree_node['right'], prune_list)
        return prune_list

        

