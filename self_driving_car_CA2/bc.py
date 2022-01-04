import os
import pandas as pd
import ntpath
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import numpy as np

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail


data_dir = '/Volumes/HADNETT/4th_Year/Smart Tech/CA2_Data'
columns = ['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed']
data = pd.read_csv(os.path.join(data_dir, 'driving_log.csv'), names=columns)
pd.set_option('max_columns', 7)
print(data.head())

data['center'] = data['center'].apply(path_leaf)
data['left'] = data['left'].apply(path_leaf)
data['right'] = data['right'].apply(path_leaf)

# Steering Data

num_bins = 25
samples_per_bin = 300
hist, bins = np.histogram(data['steering'], num_bins)
print(bins)
center = (bins[:-1] + bins[1:])*0.5
plt.bar(center, hist, width=0.05)
plt.plot((np.min(data['steering']), np.max(data['steering'])), (samples_per_bin, samples_per_bin))
plt.show()

remove_list = []
for j in range(num_bins):
    list_ = []
    for i in range(len(data['steering'])):
        if bins[j] <= data['steering'][i] <= bins[j + 1]:
            list_.append(i)
    list_ = shuffle(list_, random_state=0)
    list_ = list_[samples_per_bin:]
    remove_list.extend(list_)

print('Remove: ', len(remove_list))
data.drop(data.index[remove_list], inplace=True)
print('Remaining: ', len(data))

hist, _ = np.histogram(data['steering'], num_bins)
plt.bar(center, hist, width=0.05)
plt.plot((np.min(data['steering']), np.max(data['steering'])), (samples_per_bin, samples_per_bin))
plt.show()

print(data.iloc[1])

# Throttle Data

num_bins = 5
samples_per_bin = 420
hist, bins = np.histogram(data['throttle'], num_bins)
print(bins)
center = (bins[:-1] + bins[1:])*0.5
plt.bar(center, hist, width=0.05)
plt.plot((np.min(data['throttle']), np.max(data['throttle'])), (samples_per_bin, samples_per_bin))
plt.show()

# Indexes where changed after previous delete. Therefore, they needed to be reset in order to preform
# an additional delete. https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html
remove_list = []
data = data.reset_index(drop=True)
for j in range(num_bins):
    list_ = []
    for i in range(len(data['throttle'])):
        if bins[j] <= data['throttle'][i] <= bins[j + 1]:
            list_.append(i)
    list_ = shuffle(list_)
    list_ = list_[samples_per_bin:]
    remove_list.extend(list_)

print('Remove: ', len(remove_list))
data.drop(data.index[remove_list], inplace=True)
print('Remaining: ', len(data))

hist, _ = np.histogram(data['throttle'], num_bins)
plt.bar(center, hist, width=0.05)
plt.plot((np.min(data['throttle']), np.max(data['throttle'])), (samples_per_bin, samples_per_bin))
plt.show()

print(data.iloc[1])
