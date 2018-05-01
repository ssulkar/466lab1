import sys
import csv
import json
import xml.etree.ElementTree as ET

import logging
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(args):
    logger.debug('args: %s' % args)

if __name__=='__main__':
    if len(sys.argv) < 3:
        print('Invalid args')

    args = sys.argv
    main(args)