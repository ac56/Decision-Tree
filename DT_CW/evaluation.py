import setup
import pandas as pd
import build_tree
import predict
import assess

def evaluate_tree (train_df, n_partitions):
    part_len = int(len(train_df) / 10)
    # print('the train dataframe is:')
    # print (train_df)
    # print ('and is ' + str(len(train_df)) + " long")
    depths_total = 0
    scores_total = 0
    for i in range(n_partitions):
        test_begin = i * part_len
        test_end = test_begin + part_len
        # print('test_begin:\t' + str(test_begin))
        # print('test_end:\t' + str(test_end))
        test_part = train_df.iloc[test_begin:test_end, :]
        train_part = train_df.drop(train_df.index[test_begin:test_end])
        # print('the test part is:')
        # print(test_part)
        # print('the train part is')
        # print(train_part)
        # print('\n' * 5)
        train_part.reset_index(drop = True, inplace = True)
        answers = test_part[setup.label]
        answers.reset_index(drop = True , inplace = True)
        test_part = test_part.drop([setup.label], axis = 1)
        tree_info = tuple()
        tree_info = build_tree.decision_tree_learning(train_part, 0)
        depths_total += tree_info[1]
        # print('current tree:')
        # print(tree_info[0])
        # print('tree_info[1]:')
        # print(tree_info[1])
        prediction_list = []
        for index, row in test_part.iterrows():
            predicted_label = predict.predict_label ( tree_info[0], row)
            prediction_list.append(predicted_label)
        score = assess.set_score (prediction_list, answers)
        scores_total += score
        #print ( 'score for test_data with index ' + str(test_begin) + ' to ' + str(test_end) + ' is ' + str (score) + '%')
    print (('\n' * 5) +  'the average depth is ' + str(depths_total/ n_partitions))
    print ('the average score is ' + str(scores_total/n_partitions) + '%')
