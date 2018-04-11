import csv
# import pandas

def main():
    minsup = 0.0
    filename = 'data.csv'
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
	data = [map(str.strip, row) for row in reader]
    print data

if __name__ == '__main__':
    main()
