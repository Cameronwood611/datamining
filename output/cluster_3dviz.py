from pickletools import read_string1

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


def show_dataset(dataset, title):
    x, y, z, clusters = dataset

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, -z, zdir='z', c=clusters)
    ax.title.set_text(title)
    plt.savefig(title + ".png")
    plt.show()


def read_csv(file: str):
    df = pd.read_csv(file)
    print(df.keys())
    x, y, z, labels= df['x'], df['y'], df['z'], df['cluster']
    return x, y, z, labels


d = read_csv("random.csv")
d2 = d = read_csv("kmeans++.csv")
show_dataset(d, "Textbook K-Means")
show_dataset(d2, "kmeans++")
