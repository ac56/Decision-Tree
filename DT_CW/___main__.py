import time
import setup
import build_tree
import evaluation

start = time.time()
print ("hello")
tree, depth = build_tree.decision_tree_learning(setup.train_df, setup.depth)
time_stamp = time.time() - start
print('time elapsed to build tree:')
print(time_stamp)
print('\n')
#decided_splits_list = []
#print(tree)

evaluation.evaluate_tree( setup.train_df, 10)