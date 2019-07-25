import pandas as pd
import numpy as np


clean_array = np.loadtxt('noisy_dataset.txt')
attr_list = ['wifi1', 'wifi2', 'wifi3','wifi4', 'wifi5', 'wifi6', 'wifi7', 'room']
label = 'room'
train_df = pd.DataFrame(clean_array, columns = attr_list)
depth = 0