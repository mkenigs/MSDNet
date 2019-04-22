import MySQL_Connector as MC
import Genre_Classifier as GC
import word2vec as w2v
import Parse_Query as PQ
import numpy as np
from keras.callbacks import TensorBoard
from time import time


import os

# USER_INPUT_QUERY_FOR_WORDS = 'SELECT word FROM words LIMIT 100'

def train(select_features):
    msd, mxm, mbzdb = MC.connect_to_database()
    feature_query = PQ.get_features(where_clause='year>1960 and year<2000', table='megarelation',
                                    select_features=select_features)

    features = MC.get_output_from_database(database=msd, query=feature_query)
    track_ids = [data_point[0] for data_point in features]
    ground_truth_year = np.array([data_point[-1] for data_point in features])
    ground_truth_year = np.reshape(ground_truth_year, (len(track_ids), -1))
    features = [data_point[1:-1] for data_point in features]
    features = np.array(features)

    if features.shape[0] < 500:
        print('You have less than 500 data points. Consider loosening your constraints.')

    song_lyrics = []

    for i, track in enumerate(track_ids):
        print('searching track %s /%s' %(i, len(track_ids)-1))
        lyrics_query = PQ.get_lyrics(where_clause='track_id =' + "'" + track + "'", table='lyrics')
        lyrics = MC.get_output_from_database(database=mxm, query=lyrics_query)
        song_lyrics.append(lyrics)

    n = len(track_ids)
    p = len(features[0]) + 50
    X = np.zeros([n,p])

    for i, lyrics in enumerate(song_lyrics):
        print('vectorizing track %s /%s' %(i, len(track_ids)-1))
        if lyrics:
            word_vectors = np.array(w2v.vectorize_bag_of_words(lyrics))
        else:
            word_vectors = np.random.randn(1, 50)
    # for every row, 0~49 is word vector mean sum
        row = np.sum(word_vectors, 0) / (word_vectors.shape[0])  # gets the sum of all word embeddings
        row = np.concatenate([row, features[i]])
        X[i] = row



    # 90 / 10 train to test ratio
    train_size = int(X.shape[0]*0.9)
    trainX = X[:train_size]
    trainY = ground_truth_year[:train_size]

    testX = X[train_size:-1]
    testY = ground_truth_year[train_size:-1]


    ########################################################################################
    nn = GC.model(ground_truth_year.shape[0])
    tensorboard = TensorBoard(log_dir="logs/{}".format(time()))
    nn.fit(trainX, trainY, epochs=1000, callbacks=[tensorboard], verbose=1)
    nn.evaluate(testX, testY)







