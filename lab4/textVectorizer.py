import logging
logging.basicConfig(level=logging.DEBUG)

import sys
import os
from pprint import pprint as pp

import vector
import parse

def main(args):
    log = logging.getLogger()
    out_dir = str(args[1])
    file_list = args[2:]

    doc_col = parse.get_doc_collection(file_list)

    log.info('len(doc_list): %s' % len(doc_col.doc_list))
    log.info('len(author_list): %s' % len(doc_col.author_list))
    log.info('len(vocab): %s' % len(doc_col.vocab))

    v = vector.VectorCollection(doc_col)
    v.compute_TF_IDF()

    log.info('shape: %s' % str(v.tf_idf_table.shape))

    v.save_to_dir(out_dir)
    log.info('saved array to: %s' % out_dir)

if __name__=='__main__':
    args = sys.argv
    main(args)