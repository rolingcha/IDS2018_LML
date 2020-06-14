# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:52:34 2020

@author: USER
"""
import numpy as np
# import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


import keras
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense

import ids2018_data_set_wrangling as ids_wrangling

def create_model(p_input_shape=(0,), optimizer='adam', activation = 'relu'):
    # Initialize the constructor
    model = Sequential()
    # Add an input layer
    model.add(Dense(25, activation=activation, input_shape=p_input_shape))
    keras.layers.Dropout(0.2, noise_shape=None, seed=None)
    # Add one hidden layer
    model.add(Dense(25, activation=activation))
    keras.layers.Dropout(0.2, noise_shape=None, seed=None)
    model.add(Dense(25, activation=activation))
    keras.layers.Dropout(0.2, noise_shape=None, seed=None)
    # Add an output layer
    model.add(Dense(15, activation="softmax"))
    #compile model
    model.compile(loss='categorical_crossentropy', optimizer=optimizer,
    metrics=['accuracy'])
    return model

# %% do_processing
def do_processing():
    working_df = ids_wrangling.get_data_set('5K')
    
    # _ric_debugging_ print(input_df.keys())
    # _ric_debugging_ print(input_df.describe())
    
    X = working_df.iloc[:,0:-1]
    raw_y = working_df.iloc[:,-1:]
    
    row_col_value_exceed_float64 = np.where(X.values >= np.finfo(np.float64).max)
    rows_with_value_exceed_float64 = np.unique(row_col_value_exceed_float64[0])
    X = X.drop(index=rows_with_value_exceed_float64)

    y_encoder = LabelEncoder()
    y_encoder.fit(raw_y)
    encoded_y = y_encoder.transform(raw_y)
    
    # Converts a class vector (integers) to binary class matrix.
    binary_classes_y = np_utils.to_categorical(encoded_y)
    
    y = binary_classes_y
    
    # checking cleaning process 
    #samples_coord_max_float_exceded = 
     #   np.where(X.values >= np.finfo(np.float64).max)
    
    print(np.any(np.isnan(X)))
    print(np.all(np.isfinite(X)))

    # feature scaling
    sc_X = StandardScaler()
    X = sc_X.fit_transform(X)
    
    print("X Scaled")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
        
    print("test splited")

    classifier = create_model(p_input_shape=(30,))
    print("model defined")
    classifier.fit(X_train, y_train, batch_size=100, epochs=30)
    print("model fitted")
    y_pred = classifier.predict(X_test)
    print("prediction finished")

    
    
# %% main
if __name__ == "__main__":
    do_processing()