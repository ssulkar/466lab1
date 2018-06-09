import parseCSV as parse
import selectSplittingAttribute as split
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python induceC45.py <TrainingSetFile.xml> -headerFlag")
        print("Ex: python induceC45.py tree03-20-words.xml -True")
        return

    data = parse.parseCSV(sys.argv[1], sys.argv[2].strip('-') == 'True')
    D = data[0]
    A = data[1]
    C = A[-1]

    print(split.selectSplittingAttribute(D, A, C, 0.1))
    

if __name__ == '__main__':
    main()
