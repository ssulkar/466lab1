import sys
import csv
import math
import numpy as np
from heapq import nsmallest
'''from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as ET'''
import xml.etree.ElementTree as ET
import xml.dom.minidom

def main(args):
    if (len(args) < 2 or len(args) > 3):
        print("Usage: python3 hclustering <Filename> [<threshold>]")
        
if __name__ == '__main__':
    args = sys.argv
    main(args)
