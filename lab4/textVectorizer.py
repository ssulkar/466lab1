import logging
logging.basicConfig(level=logging.DEBUG)

import sys
import os
from pprint import pprint as pp

import vector
import parse

def main(args):
    log = logging.getLogger()
    out_dir = args[1]
    file_list = args[2:]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    doc_col = parse.get_doc_collection(file_list)

    log.info('len(vocab): %s' % len(doc_col.vocab))
    log.info('len(doc_list): %s' % len(doc_col.doc_list))

    v = vector.VectorCollection(doc_col)
    v.compute_TF_IDF()

    log.info('shape: %s' % str(v.tf_idf_table.shape))

    doc_col.save(parse.get_vocab_cache_name(out_dir), parse.get_doclist_cache_name(out_dir))
    v.save(parse.get_vector_cache_name(out_dir))
    log.info('saved array to: %s' % parse.get_vector_cache_name(out_dir))

if __name__=='__main__':
    args = sys.argv
    main(args)