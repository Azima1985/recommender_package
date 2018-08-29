# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 14:56:39 2018

@author: Mohamed Hammad
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein
from fuzzywuzzy import process
from flask import Flask,render_template
import os

movies=pd.read_csv(os.path.split(__file__)[0]+'/../data/movies.csv',index_col='movieId')
#movies.title = movies.title.apply(lambda x: x.lower())
#movies.drop('genres',axis=1,inplace=True)
ratings=pd.read_csv(os.path.split(__file__)[0]+'/../data/ratings.csv')
ratings.drop('timestamp',axis=1,inplace=True)
movies=movies.drop([ind for ind in movies.index if ind not in ratings.movieId.unique()],axis='index')
movies['number']=range(len(movies.title))
matrix = pd.pivot(ratings['userId'],ratings['movieId'],ratings['rating'].values)


#user=input('Please, enter the movies you rate highest with - in between:')
def recommend(user):   
    user_rating = [word.strip() for word in user.split('-')]
    good_movies=[]
    for m in user_rating:
        good_movies.append(process.extractOne(m,movies.title.tolist())[0])
    id_user_rating=[movies.loc[movies['title']==word]['number'] for word in good_movies]    
    user_input=np.zeros(9066)
    for i in id_user_rating:
        user_input[i]=5
    user_similarities=cosine_similarity(matrix.fillna(0).values,user_input.reshape(1,-1))
    user_similarities=pd.DataFrame(user_similarities.flatten(),index=ratings['userId'].unique())
    most_similar_users=list(user_similarities[0].sort_values(ascending=False).head(3).index)
    recommendations=[]
    for i in most_similar_users:
        recommendations.append(movies.loc[list(matrix.loc[i].sort_values(ascending=False).head(len(good_movies)).index)]['title'])
    
    final_recommendations=[]
    for i in range(len(recommendations)):
        for j in range(len(recommendations[i])):
            if recommendations[i].values[j] not in good_movies:
                final_recommendations.append(recommendations[i].values[j])
    #print('Your recommended movie(s) are:')
    return pd.Series(final_recommendations).unique()

if __name__=='__main__':
    user=input('Please, enter the movies you rate highest with - in between:')
    print('Your recommended movie(s) are:')
    print(recommend(user))