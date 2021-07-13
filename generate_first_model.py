import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras import Model
import numpy as np

model = keras.Sequential(
    [
        keras.Input(shape=(11,)),
        layers.Dense(256, activation="relu"),
        layers.Dense(3, activation="softmax"),
    ]
)
model.summary()
model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(0.01))
a=np.array([
    [1,1,0,1,0,0,0,0,0,0,0],
    [1,1,0,0,1,0,0,0,0,0,0],
    [1,1,0,0,0,1,0,0,0,0,0],
    [1,1,0,0,0,0,1,0,0,0,0],
])
y=np.array([[0,0,1],
           [0,0,1],
           [0,0,1],
           [0,0,1]])
model.fit(a,y)
a=np.array([
    [1,0,1,1,0,0,0,0,0,0,0],
    [1,0,1,0,1,0,0,0,0,0,0],
    [1,0,1,0,0,1,0,0,0,0,0],
    [1,0,1,0,0,0,1,0,0,0,0],
])
y=np.array([[0,1,0],
           [0,1,0],
           [0,1,0],
           [0,1,0]])
model.fit(a,y)
model.fit(a,y)
model.save('snake_neural.h5')