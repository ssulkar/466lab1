#Lab 3

Authors: Devon Martin, Shiv Sulkar
Emails:
- dmart112@calpoly.edu
- ssulkr@calpoly.edu

#Usage

##K-Means

python3 kmeans.py <data.csv> <k>

###Options

-i <x_index> <y_index>
Creates a 2D scatter plot of the clusters. x_index and y_index specify what
columns should be used when graphing in 2D.

-a
Creates all possible 2D graphs given the dimensions of the data. Useful for getting a feel
for a dataset

##Hierarchical

python3 hierarchical.py <data.csv> <threshold>

##DBSCAN

python3 dbscan.py <data.csv> <epsilon> <num_points>

###Options

-i <x_index> <y_index>
Creates a 2D scatter plot of the clusters. x_index and y_index specify what
columns should be used when graphing in 2D.

-c
Specifies whether circles (where radius = epsilon) should be drawn around points in a cluster
on the graph. Used with -i