#Lab 6

Authors: Devon Martin, Shiv Sulkar
Emails:
- dmart112@calpoly.edu
- ssulkar@calpoly.edu

#Usage

##EvaluateCFRandom.py
python3 EvaluateCFRandom.py <jesterfile> <method> <test_size> <repeat>

EXAMPLE:
python3 EvaluateCFRandom.py data/jester-data-1.csv cosine_adjusted 3 3


##EvaluateCFList.py
python3 EvaluateCFList.py <jesterfile> <method> <testfile>

EXAMPLE:
python3 EvaluateCFList.py data/jester-data-1.csv cosine_adjusted tests/test01.csv


# METHODS SUPPORTED: default_voting, cosine, cosine_adjusted
