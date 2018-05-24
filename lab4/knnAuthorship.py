import logging
logging.basicConfig(level=logging.INFO)

import sys
from pprint import pprint as pp

import vector
import parse
import knn

def main(args):
    log = logging.getLogger()
    in_dir = args[1]
    k = int(args[2])
        
    doc_col = parse.DocumentCollection()
    doc_col.load(parse.get_vocab_cache_name(in_dir), parse.get_doclist_cache_name(in_dir))
    v = vector.VectorCollection(doc_col)
    v.load(parse.get_vector_cache_name(in_dir))
    
    log.info('loaded array from: %s' % parse.get_vector_cache_name(in_dir))
    log.info('len(vocab): %s' % len(doc_col.vocab))
    log.info('len(doc_list): %s' % len(doc_col.doc_list))
    log.info('shape: %s' % str(v.tf_idf_table.shape))

    classifier = knn.KNNClassifier()    
    classifier.train(v.tf_idf_table, k)
    pp(classifier.clusters)

if __name__=='__main__':
    args = sys.argv
    main(args)