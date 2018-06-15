import parseCSV as parse
import selectSplittingAttribute as split
import sys

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    if len(sys.argv) < 3:
        print("Usage: python induceC45.py <TrainingSetFile.xml> -headerFlag")
        print("Ex: python induceC45.py tree03-20-words.xml -True")
        return

    logger.info('Started parsing')

    # data, labels = parse.parseCSV(sys.argv[1], sys.argv[2].strip('-') == 'True')
    data, labels = parse.parseCSV(sys.argv[1], True)

    logger.info('Finished parsing')

    # data is a list of dictionaries for each row, keys are attributes
    # D = data[0]
    D = data
    # A = data[1]
    A = labels
    C = A[-1]

    logger.info('Started algorithm')
    attrib = split.selectSplittingAttribute(D, A, C, 0.1)
    logger.info('attrib: %s' % attrib)
    logger.info('Finished algorithm')

if __name__ == '__main__':
    main()
