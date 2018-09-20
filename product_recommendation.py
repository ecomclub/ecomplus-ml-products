import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas.plotting
from surprise import SVD, Dataset, Reader, KNNBasic, accuracy
from surprise.model_selection import cross_validate
import csv
import time
import sys

# -- cont time execution

initial = time.time()

# -- open csv for analyse

df= pd.read_csv(sys.argv[1],encoding='iso-8859-1')
df.head()
df.shape
df.head()

# -- filter data for analyse

df.drop(df[df.resource_type>1].index ,inplace=True)

df.head()

# -- categorization of data

def categoriza(s):
    if s <= 14:
        return 1
    elif s >= 15 and s<=18:
        return 2
    elif s >=19 and s<=21:
        return 3
    elif s >= 15 and s<=18:
        return 4
    elif s >=22 and s<=26:
        return 5
    elif s >=31 and s<=35:
        return 6
    elif s >=36 and s<=40:
        return 7
    elif s >=41 and s<=50:
        return 8
    elif s >=50 and s<=60:
        return 9
    elif s >=61 and s<=80:
        return 10
    elif s >=81:
        return 11

# -- defining id for categorized data

df['age_range'] = df['age'].apply(categoriza)
df.head()

# -- reading category dictionary

df_profile = pd.read_csv('profile.csv')
df_profile.head()

# -- merge dictionary with data filter

df = pd.merge(df_profile,df)
df.head()

# -- drop unnecessary columns

df.drop(['browser'], axis=1, inplace=True)
df.drop(['date_time'], axis=1, inplace=True)
df.drop(['device_type'], axis=1, inplace=True)
df.drop(['os'], axis=1, inplace=True)
df.drop(['country'], axis=1, inplace=True)
df.drop(['utm_campaign'], axis=1, inplace=True)
df.drop(['utm_medium'], axis=1, inplace=True)
df.drop(['utm_source'], axis=1, inplace=True)
df.drop(['utm_term'], axis=1, inplace=True)
df.drop(['ip_addr'], axis=1, inplace=True)
df.drop(['region'], axis=1, inplace=True)
df.drop(['age_range'], axis=1, inplace=True)
df.drop(['gender'], axis=1, inplace=True)
df.drop(['age'], axis=1, inplace=True)
df.drop(['resource_type'], axis=1, inplace=True)

# -- let's set 1 for purchased

df.head()

df.id_profile.unique()

df['rating'] = 1

df.head()

list_store=df.store_id.unique()

# -- output csv

with open(sys.argv[2], 'w') as csvfile:
    writer = csv.writer(csvfile)

# -- beginning of machine learning

    for i in range(len(list_store)):
        print(list_store[i])

# -- creating unique store dataframe

        df_result=df[df['store_id']==list_store[i] ]

# -- 1 bought and 0 not purchased

        reader = Reader(rating_scale=(0,1))

# -- load dataframe filtered

        data = Dataset.load_from_df(df_result[['id_profile','resource_id','rating']], reader=reader)

# -- These are algorithm that are directly derived from a basic nearest neighbors approach.

        algo_kNN  = KNNBasic(sim_options = {'name':'cosine', 'user_based': False})
        cross_validate(algo_kNN, data, measures=['RMSE','MAE'], cv = 5, verbose = True)
        algo_SVD  = SVD()

# -- matrix factorization algorithm

        cross_validate(algo_SVD, data, measures=['RMSE','MAE'], cv = 5, verbose = True)
        trainset = data.build_full_trainset()
        testset = trainset.build_anti_testset()
        algo = SVD()
        algo.fit(trainset)

        prediction = algo.test(testset)

        prediction[:3]

# -- maximum number of products
        n = 100

# -- Here create a pseudolist

        top_n = defaultdict(list)
        for uid, iid, r_ui, est, _ in prediction:
            top_n[uid].append((iid,est))
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse = True)
            top_n[uid] = user_ratings[:n]

# -- print data

        for uid, user_ratings in top_n.items():
            writer.writerow([list_store[i], uid,[iid for (iid, _) in user_ratings]])
            #print(uid, [iid for (iid, _) in user_ratings])

endtime = time.time()
print ("execution time: ", endtime-initial)
