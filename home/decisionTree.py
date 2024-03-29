#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 19:30:33 2022

@author: ubuntu
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing

df = pd.read_csv('formatted_log.csv')

df["startTime"] = pd.to_datetime(df["startTime"], format='%Y-%m-%d %H:%M:%S')
df['startTime_year'] = df["startTime"].dt.year
df['startTime_month'] = df["startTime"].dt.month
df['startTime_day'] = df["startTime"].dt.day
df['startTime_hour'] = df["startTime"].dt.hour
df['startTime_minute'] = df["startTime"].dt.minute
df['startTime_second'] = df["startTime"].dt.second

df["endTime"] = pd.to_datetime(df["endTime"], format='%Y-%m-%d %H:%M:%S')
df['endTime_year'] = df["endTime"].dt.year
df['endTime_month'] = df["endTime"].dt.month
df['endTime_day'] = df["endTime"].dt.day
df['endTime_hour'] = df["endTime"].dt.hour
df['endTime_minute'] = df["endTime"].dt.minute
df['endTime_second'] = df["endTime"].dt.second

df["h1time"] = pd.to_datetime(df["h1time"], format='%Y-%m-%d %H:%M:%S', errors='coerce')
try:
    df['h1time_year'] = df["h1time"].dt.year
    df['h1time_month'] = df["h1time"].dt.month
    df['h1time_day'] = df["h1time"].dt.day
    df['h1time_hour'] = df["h1time"].dt.hour
    df['h1time_minute'] = df["h1time"].dt.minute
    df['h1time_second'] = df["h1time"].dt.second
except:
    df['h1time_year'] = 0
    df['h1time_month'] = 0
    df['h1time_day'] = 0
    df['h1time_hour'] = 0
    df['h1time_minute'] = 0
    df['h1time_second'] = 0

df["h2time"] = pd.to_datetime(df["h2time"], format='%Y-%m-%d %H:%M:%S', errors='coerce')
try:
    df['h2time_year'] = df["h2time"].dt.year
    df['h2time_month'] = df["h2time"].dt.month
    df['h2time_day'] = df["h2time"].dt.day
    df['h2time_hour'] = df["h2time"].dt.hour
    df['h2time_minute'] = df["h2time"].dt.minute
    df['h2time_second'] = df["h2time"].dt.second
except:
    df['h2time_year'] = 0
    df['h2time_month'] = 0
    df['h2time_day'] = 0
    df['h2time_hour'] = 0
    df['h2time_minute'] = 0
    df['h2time_second'] = 0

df['h1time_year'] = df['h1time_year'].fillna(0)
df['h1time_month'] = df['h1time_month'].fillna(0)
df['h1time_day'] = df['h1time_day'].fillna(0)
df['h1time_hour'] = df['h1time_hour'].fillna(0)
df['h1time_minute'] = df['h1time_minute'].fillna(0)
df['h1time_second'] = df['h1time_second'].fillna(0)

df['h2time_year'] = df['h2time_year'].fillna(0)
df['h2time_month'] = df['h2time_month'].fillna(0)
df['h2time_day'] = df['h2time_day'].fillna(0)
df['h2time_hour'] = df['h2time_hour'].fillna(0)
df['h2time_minute'] = df['h2time_minute'].fillna(0)
df['h2time_second'] = df['h2time_second'].fillna(0)


def get_sec(time_str):
    time = time_str.split(':')
    if len(time) == 3:
        x = (int(time[0]) * 3600) + (int(time[1]) * 60) + int(float(time[2]))
        return x
    else:
        return time_str


df['diffh1_second'] = df['diffh1'].apply(get_sec)
df['diffh2_second'] = df['diffh2'].apply(get_sec)
df['time_second'] = df['time'].apply(get_sec)

label_encoder = preprocessing.LabelEncoder()

df['chapter'] = label_encoder.fit_transform(df['chapter'])
df['chapter'].unique()

df['levelofdifficulty'] = label_encoder.fit_transform(df['levelofdifficulty'])
df['levelofdifficulty'].unique()

df['qid'] = label_encoder.fit_transform(df['qid'])
df['qid'].unique()

X = df[['hintCount', 'qcount', 'chapter', 'levelofdifficulty', 'wrongCount',
        'wronghintcount', 'time_second']]

Y = df['score']

X_train, X_test, y_train, y_test = train_test_split(
    X, Y,
    test_size=0.3,
    random_state=100)

# Function to perform training with giniIndex.
clf_gini = DecisionTreeClassifier(criterion="gini", random_state=100, max_depth=3, min_samples_leaf=5)
clf_gini.fit(X_train, y_train)
# y_pred = clf_gini.predict(X_test)
pickle.dump(clf_gini, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))
# accuracy_score_gini = accuracy_score(y_test, y_pred) * 100
# print(accuracy_score_gini)

# clf_entropy = DecisionTreeClassifier(
#     criterion="entropy", random_state=100,
#     max_depth=3, min_samples_leaf=5)
# clf_entropy.fit(X_train, y_train)
# y_pred_ent = clf_entropy.predict(X_test)
# accuracy_score_ent = accuracy_score(y_test, y_pred_ent) * 100
# print(accuracy_score_ent)

