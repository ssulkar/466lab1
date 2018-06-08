import sys
import csv
import numpy
import math
import random

#IMPORTANT: user_ids and item_ids both start at id 0

def main():
    filename = sys.argv[1]
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

    
    #print(items)
    #print()
    #print(users)
    test_list = create_test(users, 1)
    print(test_list) 
    user_id = test_list[0][0]
    item_id = test_list[0][1]
    actual = get_item_rating(users, user_id, item_id)
    
    print(actual)
    cosine_similarity_adjusted(users, items, user_id, item_id)
    
    
def create_test(users, test_size):
    test_list = []
    for i in range(test_size):
        user_id = random.randint(0, len(users)-1)
        user = users[user_id]
        
        rating_list = user["user_ratings_list"]
        item_id = random.randint(0, len(rating_list)-1)
        rating = rating_list[item_id]
        while (rating == 99.0):
            user_id = random.randint(0, len(users)-1)
            user = users[user_id]
        
            rating_list = user["user_ratings_list"]
            item_id = random.randint(0, len(rating_list)-1)
            rating = rating_list[item_id]
        test_list.append([user_id, item_id])
    return test_list    
   
def get_item_rating(users, user_id, item_id):
    user = users[user_id]
    rating_list = user["user_ratings_list"]
    rating = rating_list[item_id]
    return rating

def weighted_sum(users, items, user_id, item_id):
    numer = 0 
    denom = 0
    user = users[user_id]
    avg_user_rating = user["avg_user_rating"]
    
    for other_user in users:
        rating = other_user["user_ratings_list"][item_id]
        #make sure the user isn't the same and also that their rating isn't null (99)
        if other_user["user_id"] != user_id and rating != 99.0:
            
            sim = cosine(user["user_ratings_list"], other_user["user_ratings_list"])
            #sim = pearson(user["user_ratings_list"], other_user["user_ratings_list"])
            
            denom += abs(sim)
            numer += sim * (rating - avg_user_rating)
    print(numer/denom)
    return numer/denom
    
def default_voting(users, items, user_id, item_id):
    numer = 0 
    denom = 0
    user = users[user_id]
    avg_user_rating = user["avg_user_rating"]
    
    for other_user in users:
        rating = other_user["user_ratings_list"][item_id]
        #make sure the user isn't the same and also that their rating isn't null (99)
        if other_user["user_id"] != user_id and rating != 99.0:
            sim = 1
            n = 0
            sum1 = 0
            sum2 = 0
            sq1 = 0
            sq2 = 0
            p = 0
            rating_list1 = user["user_ratings_list"]
            rating_list2 = other_user["user_ratings_list"]
    
            for i in range(len(rating_list1)):
                rating1 = rating_list1[i]
                rating2 = rating_list2[i]
                if(rating1 != 99.0) and (rating2 != 99.0):
                    n += 1
                    sum1 += rating1
                    sum2 += rating2
                    sq1 += rating1 ** 2.0
                    sq2 += rating2 ** 2.0
                    p += rating1 * rating2
            den = math.sqrt((sq1 - sum1**2 / n) * (sq2 - sum2**2 / n))

            if den != 0:
                #(1/k)
                sim = p - (sum1*sum2 / n)/den
    
            denom += abs(sim)
            numer += sim * (rating - avg_user_rating)
    print(numer/denom)
    return numer/denom    
    
def cosine_similarity_adjusted(users, items, user_id, item_id):
    numer = 0 
    denom = 0
    user = users[user_id]
    avg_user_rating = user["avg_user_rating"]
    outsim = 0
    
    for other_user in users:
        rating = other_user["user_ratings_list"][item_id]
        #make sure the user isn't the same and also that their rating isn't null (99)
        if other_user["user_id"] != user_id and rating != 99.0:
            sim = 1
            rating_list1 = user["user_ratings_list"]
            rating_list2 = other_user["user_ratings_list"]
            numerator = numpy.dot(rating_list1, rating_list2) 
            denominator = (math.sqrt(numpy.dot(rating_list1, rating_list1)) * math.sqrt(numpy.dot(rating_list2, rating_list2)))
            if(denominator != 0):
                sim = numerator/denominator
            denom += abs(sim)
            numer += sim * (rating - avg_user_rating)
    print(numer/denom)
    return numer/denom
    
def cosine_similarity(users, items, user_id, item_id):
    numer = 0 
    denom = 0
    user = users[user_id]
    
    for other_user in users:
        rating = other_user["user_ratings_list"][item_id]
        #make sure the user isn't the same and also that their rating isn't null (99)
        if other_user["user_id"] != user_id and rating != 99.0:
            sim = 1
            rating_list1 = user["user_ratings_list"]
            rating_list2 = other_user["user_ratings_list"]
            numerator = numpy.dot(rating_list1, rating_list2) 
            denominator = (math.sqrt(numpy.dot(rating_list1, rating_list1)) * math.sqrt(numpy.dot(rating_list2, rating_list2)))
            if(denominator !=0):
                sim = numerator/denominator
            denom += abs(sim)
            numer += sim * rating
            
    print(numer/denom)
    return numer/denom
  
if __name__ == '__main__':
    main()
