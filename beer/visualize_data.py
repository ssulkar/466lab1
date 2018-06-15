import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import csv

def main():
    filename = './datasets/craft-cans/beers_clean.csv'
    abv_col = 1
    ibu_col = 2
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
    data = data[data[:, ibu_col] != '']
    data = data[data[:, style_col] != '']

    styles = np.unique(data[:, style_col])
    subsets = {key: [] for key in styles}
    for row in data:
        subsets[row[style_col]].append(row)

    # for k in sorted(subsets):
    #     data = np.asarray(subsets[k])
    #     if (len(data) > threshold):
    #         abv = data[:, abv_col].astype(float)
    #         ibu = data[:, ibu_col].astype(float)
    #         labels = data[:, style_col]

    #         fig = plt.figure(figsize=(10,5))
    #         plt.xlabel('ABV')
    #         plt.ylabel('IBU')
            
    #         plt.scatter(abv, ibu, label=labels, s=50, alpha=.5)
    #         fig.tight_layout()
    #         fig.savefig('beers_' + str(k).replace(' ', '_').replace('/', '_') + '.png')
    #         plt.close(fig)
    
    fig_all = plt.figure(figsize=(10,5))
    plt.xlabel('ABV')
    plt.ylabel('IBU')
    for k in sorted(subsets):
        data = np.asarray(subsets[k])
        if (len(data) > threshold):
            abv = data[:, abv_col].astype(float)
            ibu = data[:, ibu_col].astype(float)
            labels = data[:, style_col]
            plt.scatter(abv, ibu, label=labels, s=50, alpha=.5)

    fig_all.tight_layout()
    fig_all.savefig('all_beers_abv_ibu.png')
    plt.close(fig_all)

    


if __name__ == '__main__':
    main()