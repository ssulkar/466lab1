import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import csv

def main():
    filename = './datasets/craft-cans/beers_clean.csv'
    abv_col = 1
    ibu_col = 2
    ounces_col = 7
    style_col = 5

    # filename = './datasets/beer-recipes/recipeData.csv'
    # abv_col = 8
    # ibu_col = 9
    # style_col = 3

    threshold = 10

    data = None
    with open(filename, 'r', encoding='latin-1') as f:
        data = np.array(list(csv.reader(f))[1:])

    data = data[data[:, abv_col] != '']
    data = data[data[:, ounces_col] != '']
    data = data[data[:, style_col] != '']

    styles = np.unique(data[:, style_col])
    subsets = {key: [] for key in styles}
    for row in data:
        subsets[row[style_col]].append(row)

    fig_all = plt.figure(figsize=(10,5))
    plt.xlabel('Ounces')
    plt.ylabel('ABV')
    for k in sorted(subsets):
        data = np.asarray(subsets[k])
        if len(data) > threshold:
            print(len(data))
            print(k)
            abv = data[:, abv_col].astype(float)
            abv[abv > .8] = 0
            ounces = data[:, ounces_col].astype(float)
            labels = data[:, style_col]
            plt.scatter(ounces, abv, label=k, s=50, alpha=.5)

    fig_all.tight_layout()
    # plt.legend()
    fig_all.savefig('ounces_abv.png')
    plt.close(fig_all)

    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------

    data = None
    with open(filename, 'r', encoding='latin-1') as f:
        data = np.array(list(csv.reader(f))[1:])

    data = data[data[:, ibu_col] != '']
    data = data[data[:, ounces_col] != '']
    data = data[data[:, style_col] != '']

    styles = np.unique(data[:, style_col])
    subsets = {key: [] for key in styles}
    for row in data:
        subsets[row[style_col]].append(row)

    fig_all = plt.figure(figsize=(10,5))
    plt.xlabel('Ounces')
    plt.ylabel('IBU')
    for k in sorted(subsets):
        data = np.asarray(subsets[k])
        if len(data) > threshold:
            print(len(data))
            print(k)
            ibu = data[:, ibu_col].astype(float)
            ounces = data[:, ounces_col].astype(float)
            labels = data[:, style_col]
            plt.scatter(ounces, ibu, label=k, s=50, alpha=.5)

    fig_all.tight_layout()
    # plt.legend()
    fig_all.savefig('ounces_ibu.png')
    plt.close(fig_all)

    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------

    data = None
    with open(filename, 'r', encoding='latin-1') as f:
        data = np.array(list(csv.reader(f))[1:])

    data = data[data[:, ibu_col] != '']
    data = data[data[:, abv_col] != '']
    data = data[data[:, style_col] != '']

    styles = np.unique(data[:, style_col])
    subsets = {key: [] for key in styles}
    for row in data:
        subsets[row[style_col]].append(row)

    threshold = 20

    fig_all = plt.figure(figsize=(10,5))
    plt.xlabel('ABV')
    plt.ylabel('IBU')
    for k in sorted(subsets):
        data = np.asarray(subsets[k])
        # if len(data) > threshold and 'IPA' in k:
        if len(data) > threshold and 'American' in k:
            print(len(data))
            print(k)
            ibu = data[:, ibu_col].astype(float)
            abv = data[:, abv_col].astype(float)
            labels = data[:, style_col]
            plt.scatter(abv, ibu, label=k, s=50, alpha=.5)

    fig_all.tight_layout()
    plt.legend()
    fig_all.savefig('ounces_4.png')
    plt.close(fig_all)

if __name__ == '__main__':
    main()