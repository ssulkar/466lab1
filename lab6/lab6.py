import sys
import csv
import numpy


def main():
    filename = sys.argv[1]
    reader = csv.reader(open(filename, "r"), delimiter=",")
    data_list = list(reader)
    
    matrix = numpy.array(data_list).astype("float")
    #user_stats = {}
    #content_stats = {}
    
    user_stats = []
    
    #initializes dictionaries for all 100 items
    #notice it ignores the first index, that is the user's total rating count
    item_stats = [{"item_id": i, "avg_item_rating": 0, "total_item_ratings": 0} for i in range(len(matrix[0][1:]))]
    
    
    for i, row in enumerate(matrix):
        individual_user_stat = {"user_id": i, "avg_user_rating": 0, "user_ratings_list": row[1:], "total_user_ratings": row[0]}
        
        for j, rating in enumerate(row[1:]):
            if(rating != 99.0):
                #for now we will use avg_user_rating to store the sum
                individual_user_stat["avg_user_rating"] += rating
                #for now we will use avg_item_rating to store the sum
                item_stats[j]["avg_item_rating"] += rating
                #this count will later come in handy to calculate the average
                item_stats[j]["total_item_ratings"] += 1
        if(individual_user_stat["total_user_ratings"] != 0):
             individual_user_stat["avg_user_rating"] = individual_user_stat["avg_user_rating"]/individual_user_stat["total_user_ratings"]
        user_stats.append(individual_user_stat)
    
    #calculate average item rating
    for item in item_stats:
        item["avg_item_rating"] = item["avg_item_rating"]/item["total_item_ratings"]

    
    print(item_stats)
    print()
    print(user_stats)
    

    
if __name__ == '__main__':
    main()
