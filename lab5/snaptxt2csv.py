import sys

def main():
    filename = sys.argv[1]
    fileformat = '.csv'
    outfilename = filename+fileformat
    with open(filename, 'r') as inputFile, open(outfilename, 'w') as outputFile:
        for line in inputFile:
            fields = line.split()
            outputFile.write('{}\n'.format(','.join(fields)))


if __name__ == '__main__':
    main()
