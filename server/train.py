#%%
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, BatchNormalization, Activation
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.constraints import maxnorm
from keras.utils import np_utils
import tensorflow as tf
import matplotlib.pyplot as plt
seed = 21

from keras.datasets import cifar10
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

new_run = False

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = X_train / 255.0
X_test = X_test / 255.0

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
class_num = y_test.shape[1]
#%%
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=X_train.shape[1:], padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3), input_shape=(3, 32, 32), activation='relu', padding='same'))
model.add(Dropout(0.2))
model.add(BatchNormalization())
model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(BatchNormalization())
    
model.add(Conv2D(128, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(BatchNormalization())
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(256, kernel_constraint=maxnorm(3)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(BatchNormalization())
    
model.add(Dense(128, kernel_constraint=maxnorm(3)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(Dense(class_num))
model.add(Activation('softmax'))

epochs = 25
optimizer = 'adam'

model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
print(model.summary())
np.random.seed(seed)
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=64)
#%%
if new_run==True:
    model.save('my_model1.h5')
else:
    model = tf.keras.models.load_model('my_model1.h5')

scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
#%%
new_image = plt.imread('cat.jpg')
from skimage.transform import resize
resized_image = resize(new_image,(32,32,3))
predictions = model.predict(np.array([resized_image]))
list_index=[0,1,2,3,4,5,6,7,8,9]
x = predictions 

for i in range(10):
	for j in range(10):
		if x[0][list_index[i]] > x[0][list_index[j]]:
			temp = list_index[i]
			list_index[i] = list_index[j]
			list_index[j] = temp
classification = ['airplane', 'automobile', 'bird','cat','deer','dog','frog','horse','ship','truck']
predicted_value = []
for i in range(5):
	value = classification[list_index[i]] + ':' + str(round(predictions[0][list_index[i]]*100,2)) + '%'
	predicted_value.append(value)


# %%
