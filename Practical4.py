import pandas as pd 
from surprise import Dataset, Reader 
from surprise import SVD 
from surprise.model_selection import train_test_split 
from surprise import accuracy 

data = Dataset.load_builtin('ml-100k') 
reader = Reader(line_format='user item rating timestamp', sep='\t') 
df = pd.DataFrame(data.raw_ratings, columns=['user_id', 'item_id', 'rating', 'timestamp']) 
trainset, testset = train_test_split(data, test_size=0.2) 
model = SVD() 
model.fit(trainset) 
predictions = model.test(testset) 
rmse = accuracy.rmse(predictions) 
print(f'RMSE: {rmse}') 

def get_top_n_recommendations(predictions, n=10): 
    top_n = {} 
    for uid, iid, true_r, est, _ in predictions: 
        if not uid in top_n: 
            top_n[uid] = [] 
        top_n[uid].append((iid, est)) 
    for uid, user_ratings in top_n.items(): 
        user_ratings.sort(key=lambda x: x[1], reverse=True) 
        top_n[uid] = user_ratings[:n] 
    return top_n 

top_n_recommendations = get_top_n_recommendations(predictions, n=10) 
print(top_n_recommendations)