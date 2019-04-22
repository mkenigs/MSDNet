import keras

def model(feature_size):
    model = keras.Sequential()
    model.add(keras.layers.Dense(units=feature_size, activation='relu'))
    model.add(keras.layers.Dense(units=10, activation='relu'))
    model.add(keras.layers.Dense(units=6, activation='relu'))
    model.add(keras.layers.Dense(units=1, activation='softmax'))
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    return model







