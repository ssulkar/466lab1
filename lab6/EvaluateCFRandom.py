import Techniques
import sys
import csv
import numpy




#ID assignment starts at 0

def main():
    if(len(sys.argv)!=5):
        print("Usage: python3 EvaluateCFRandom.py <jesterfile> <method> <test_size> <repeat>")
        return 0
    filename = sys.argv[1]
    method = sys.argv[2]
    test_size = int(sys.argv[3])
    repeat = int(sys.argv[4])
    
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
      
    MAEs = []  
    print("method: " + method)
    for i in range(repeat):
        print("trial #" + str(i+1))
        test_list = Techniques.create_test(users, test_size)
        Techniques.create_predictions(test_list, users, method, MAEs)
    if(len(MAEs)>1):
        print("MAE Average: " + str(numpy.average(MAEs)))
        print("MAE Standard Deviation: " + str(numpy.std(MAEs, ddof=1)))
    else:
        print("MAE Average requires more than one MAE")
        print("MAE Standard Deviation requires more than one MAE.")     

if __name__ == '__main__':
    main()