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

from regressiondataset import path_img


class DatasetReg(Dataset):
    def __init__(self, path, transform = None):
        self.path = path
        self.transform = transform

        self.list_name_file = os.listdir(path)
        if 'coords.json' in self.list_name_file:
            self.list_name_file.remove('coords.json')

        self.len_dataset = len(self.list_name_file)

        with open(os.path.join(self.path, 'coords.json'), 'r') as f:
            self.dict_coords = json.load(f)

    def __len__(self):
        return  self.len_dataset

    def __getitem__(self, index):
        name_file = self.list_name_file[index]
        path_img = os.path.join(self.path, name_file)

        img = np.array(Image.open(path_img))
        coord = np.array(self.dict_coords[name_file])

        if self.transform is not None:
            img = self.transform(img)

        return img, coord

dataset = DatasetReg(Path.cwd() / 'dataset')

#print(len(dataset))

#img, coord = dataset[99999]
#print(f'Координаты центра - {coord}')
#plt.scatter(coord[0], coord[1], marker = 'o', color = 'red')
#plt.imshow(img, cmap = 'gray')
#plt.show()

train_set, val_set, test_set   = random_split(dataset, [0.7, 0.1, 0.2])

#print(len(train_set), len(val_set), len(test_set))

train_loader = DataLoader(train_set, batch_size = 64, shuffle = True)
val_loader = DataLoader(val_set, batch_size = 64, shuffle = False)
test_loader = DataLoader(test_set, batch_size = 64, shuffle = False)