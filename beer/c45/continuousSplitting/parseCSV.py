import csv

def parseCSV(fileName, headerFlag):
    dataStruct = []
    with open(fileName) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        if headerFlag:
            labels = next(csvReader)[1:]
            next(csvReader)
            next(csvReader)
            dataStruct = [createDict(x[1:], labels) for x in csvReader if len(x[1:]) == len(labels)]
        else:
            labels = ["sepal length in cm", "sepal width in cm", "petal length in cm", "petal width in cm", "class"]
            dataStruct = [createDict(x, labels) for x in csvReader if len(x) == len(labels)]
        
    return (dataStruct, labels)

def createDict(values, labels):
    dict = {}
    for i in range(len(labels)):
        dict[labels[i]] = values[i]

    return dict
