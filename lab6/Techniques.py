import math
import random
import numpy

def create_predictions(test_list, users, method, MAEs):
    if (method == "cosine_adjusted"):
        expected_list = []
        actual_list = []
        for i in range(len(test_list)):
            user_id = test_list[i][0]
            item_id = test_list[i][1]
            expected_list.append(get_item_rating(users, user_id, item_id))
            actual_list.append(cosine_similarity_adjusted(users, user_id, item_id))
        MAEs.append(print_result(test_list, expected_list, actual_list))
        
    elif (method == "cosine"):
        expected_list = []
        actual_list = []
        for i in range(len(test_list)):
            user_id = test_list[i][0]
            item_id = test_list[i][1]
            expected_list.append(get_item_rating(users, user_id, item_id))
            actual_list.append(cosine_similarity(users, user_id, item_id))
        MAEs.append(print_result(test_list, expected_list, actual_list))
    elif (method == "default_voting"):
        expected_list = []
        actual_list = []
        for i in range(len(test_list)):
            user_id = test_list[i][0]
            item_id = test_list[i][1]
            expected_list.append(get_item_rating(users, user_id, item_id))
            actual_list.append(default_voting(users, user_id, item_id))
        MAEs.append(print_result(test_list, expected_list, actual_list))
    else:
        print("Method does not exist! Available methods: cosine, cosine_adjusted, default_voting")    
    
    
def print_result(test_list, expected_list, actual_list):
    headers = ["userID", "itemID", "Actual_Rating", "Predicted_Rating", "Delta_Rating"]
    
    mu = 0
    print("{:<18} {:<18} {:<18} {:<18} {:<18}".format(*headers))
    for i in range(len(test_list)):
        user_id = str(test_list[i][0]) 
        item_id = str(test_list[i][1])
        expected = (expected_list[i])
        actual = (actual_list[i]) 
        delta = actual - expected
        line = [user_id, item_id, str(expected), str(actual), str(delta)]
        print("{:<18} {:<18} {:<18} {:<18} {:<18}".format(*line))
        mu += abs(delta)
        
    MAE = mu/len(test_list)
    print("MAE: " + str(MAE))
    print()
    return MAE  
    
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

def default_voting(users, user_id, item_id):
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
    return numer/denom    
    
def cosine_similarity_adjusted(users, user_id, item_id):
    numer = 0 
    denom = 0
    user = users[user_id]
    avg_user_rating = user["avg_user_rating"]
    
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
    
    return numer/denom
    
def cosine_similarity(users, user_id, item_id):
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
            
    return numer/denom