import sys
from pathlib import Path
from random import random

import torch
import torchvision

from torchvision.datasets import ImageFolder
from torch.utils.data import Dataset, DataLoader, random_split

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class MNISTDataset(Dataset):
    def __init__(self, path, transform = None):
        self.path = path
        self.transform = transform
        self.len_dataset = 0
        self.data_list = []

        for path_dir, dir_list, file_list in os.walk(path):
            if path_dir == path:
                self.classes = dir_list
                self.class_to_idx = {
                    cls_name :i for i, cls_name in enumerate(self.classes)
                }
                continue

            cls  = path_dir.split('\\')[-1]

            for name_file in file_list:
                file_path = os.path.join(path_dir, name_file)
                self.data_list.append((file_path, self.class_to_idx[cls]))
            self.len_dataset += len(file_list)

    def __len__(self):
        return  self.len_dataset

    def __getitem__(self, index):
        file_path, target = self.data_list[index]
        sample = np.array(Image.open(file_path))

        if self.transform is not None:
            sample = self.transform(sample)

        return sample, target

train_data = MNISTDataset(r'D:\projects\PyTorch\content\mnist\training')
test_data = MNISTDataset(r'D:\projects\PyTorch\content\mnist\testing')

#train_data = ImageFolder(Path.cwd() / 'content/mnist/training')
#test_data = ImageFolder(Path.cwd() / 'content/mnist/testing')

test1 = train_data.classes
test2 = train_data.class_to_idx

#print(test1, test2, len(train_data), len(test_data),sep= '\n\n')
#img, one_hot_position = train_data[59999]
#cls = train_data.classes[one_hot_position]
#print(f'Класс - {cls}')
#plt.imshow(img, cmap = 'gray')
#plt.show()

train_data, val_data = random_split(train_data, [0.8, 0.2])

#print(len(train_data), len(val_data), len(test_data))

train_loader = DataLoader(train_data, batch_size = 16, shuffle = True)
val_loader = DataLoader(val_data, batch_size = 16, shuffle = False)
test_loader = DataLoader(test_data, batch_size = 16, shuffle = False)