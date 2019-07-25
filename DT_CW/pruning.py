import setup
import pandas as pd
import build_tree
import predict
import assess
import copy


def prune_tree(tree_node, valid_set):
    valid_answers = valid_set[setup.label]
    # print ('valid answers before resetting index:')
    # print(valid_answers)
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
        temp_node = copy.deepcopy(prune)
        prune['attr'] = setup.label
        prune['left'] = None
        prune['right'] = None
        prune['leaf'] = True

        prune['value'] = temp_node['left']['value']
        valid_prediction_list =[]
        for index, row in valid_set.iterrows():
            predicted_label = predict.predict_label ( tree_node, row)
            valid_prediction_list.append(predicted_label)
        left_score = assess.set_score(valid_prediction_list, valid_answers)

        prune['value'] = temp_node['right']['value']
        valid_prediction_list = []
        for index, row in valid_set.iterrows():
            predicted_label = predict.predict_label ( tree_node, row)
            valid_prediction_list.append(predicted_label)
        right_score = assess.set_score(valid_prediction_list, valid_answers)
        # print('\nprevious score:\t' + str(previous_score) )
        # print('left score:\t' + str(left_score))
        # print('right score:\t' + str(right_score))
        if( (left_score >= previous_score) or (right_score >= previous_score) ):
        # print('tree has been pruned')
            if (left_score > right_score):
                prune['value'] = temp_node['left']['value']
        # print('new value is left branch value')
        #     else:
        # #print('new value is right branch value')
        else:
            prune = temp_node
        #print('prune denied')

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

        

