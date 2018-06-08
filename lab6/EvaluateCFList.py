import Techniques
import sys
import csv
import numpy

#ID assignment starts at 0

def main():
    if(len(sys.argv)!=4):
        print("Usage: python3 EvaluateCFList.py <jesterfile> <method> <testfile>")
        return 0
    filename = sys.argv[1]
    method = sys.argv[2]
    testfilename = sys.argv[3]
    repeat = 1

    reader = csv.reader(open(filename, "r"), delimiter=",")
    data_list = list(reader)
    
    
    matrix = numpy.array(data_list).astype("float")
    
    users = []
    
    #initializes dictionaries for all 100 items
    #notice it ignores the first index, that is the user's total rating count
    items = [{"item_id": i, "avg_item_rating": 0, "total_item_ratings": 0} for i in range(len(matrix[0][1:]))]
    
    
    for i, row in enumerate(matrix):
        individual_user = {"user_id": i, "avg_user_rating": 0, "user_ratings_list": row[1:], "total_user_ratings": row[0]}
        
        for j, rating in enumerate(row[1:]):
            if(rating != 99.0):
                #for now we will use avg_user_rating to store the sum
                individual_user["avg_user_rating"] += rating
                #for now we will use avg_item_rating to store the sum
                items[j]["avg_item_rating"] += rating
                #this count will later come in handy to calculate the average
                items[j]["total_item_ratings"] += 1
        if(individual_user["total_user_ratings"] != 0):
             individual_user["avg_user_rating"] = individual_user["avg_user_rating"]/individual_user["total_user_ratings"]
        users.append(individual_user)
    
    #calculate average item rating
    for item in items:
        item["avg_item_rating"] = item["avg_item_rating"]/item["total_item_ratings"]
    
    testreader = csv.reader(open(testfilename, "r"), delimiter=",")
    test_list = list(testreader)
    test_list = numpy.array(test_list).astype("int")
    for i in range(len(test_list)):
        uid = test_list[i][0]
        iid = test_list[i][1]
        rating = Techniques.get_item_rating(users, uid, iid)
        if(rating == 99.0):
            print("Rating at user id " + str(uid) +" and item id " + str(iid) + " is 99. Fix your test.")
            return 0
    for i in range(repeat):
        Techniques.create_predictions(test_list, users, method)
        
if __name__ == '__main__':
    main()