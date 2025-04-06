import os
from pathlib import Path
import struct
from array import array
from os import path
import numpy as np
import torchvision.datasets
from PIL import Image

train_dataset = torchvision.datasets.MNIST(root = Path.cwd() / 'content/raw_mnist', train = True, download = True)
test_dataset = torchvision.datasets.MNIST(root = Path.cwd() / 'content/raw_mnist', train = False, download = True)

def read(dataset):
    if dataset is "training":
        path_img = Path.cwd() / 'content/raw_mnist/MNIST/raw/train-images-idx3-ubyte'
        path_lbl = Path.cwd() / 'content/raw_mnist/MNIST/raw/train-labels-idx1-ubyte'
    elif dataset is "testing":
        path_img = Path.cwd() / 'content/raw_mnist/MNIST/raw/t10k-images-idx3-ubyte'
        path_lbl = Path.cwd() / 'content/raw_mnist/MNIST/raw/t10k-labels-idx1-ubyte'
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    with open(path_lbl, 'rb') as f_label:
        _, size = struct.unpack(">II", f_label.read(8))
        lbl = array("b", f_label.read())

    with open(path_img, 'rb') as f_img:
        _, size, rows, cols = struct.unpack(">IIII", f_img.read(16))
        img = array("B", f_img.read())

    return lbl, img, size, rows, cols

def write_dataset(labels, data, size, rows, cols, output_dir):

    classes = {i: f"class_{i}" for i in range(10)}

    output_dirs = [
        path.join(output_dir, classes[i])
        for i in range(10)
    ]
    for dir in output_dirs:
        if not path.exists(dir):
            os.makedirs(dir)


    for (i, label) in enumerate(labels):
        output_filename = path.join(output_dirs[label], str(i) + ".jpg")
        print("writing" + output_filename)

        with open(output_filename, "wb") as h:
            data_i = [
                data[(i * rows * cols + j * cols) : (i * rows * cols + (j + 1) * cols)]
                for j in range(rows)
            ]
            data_array  = np.asarray(data_i)

            im = Image.fromarray(data_array)
            im.save(output_filename)

output_path = Path.cwd() / 'content/mnist'

for dataset in ["training", "testing"]:
    write_dataset(*read(dataset), path.join(output_path, dataset))