import time
import setup
import build_tree
import evaluation
import pruning

start = time.time()
print ("hello")
tree, depth = build_tree.decision_tree_learning(setup.train_df, setup.depth)
time_stamp = time.time() - start
print('time elapsed to build tree:')
print(time_stamp)
print('\n')
#decided_splits_list = []
#print(tree)
prune_list = []
prune_list = pruning.find_potential_prunes( tree , prune_list)
print(('\n' * 4) + 'prune_list:')
for i in range(len(prune_list)):
    print(prune_list[i])
    print('\n')
#evaluation.evaluate_unpruned( setup.train_df, 10)