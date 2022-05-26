import io
from fastapi import FastAPI, File
import numpy as np
import matplotlib.pyplot as plt
import uvicorn
import regex
import tensorflow as tf
model = tf.keras.models.load_model('my_model1.h5')

app = FastAPI(debug=True)

@app.get('/')
async def home():
    return {"Hello": "World"}

@app.post('/predict')
def predict(img: bytes = File()):
    values = give_prediction(img)

    key_values= {}
    for value in values:
        match = regex.match(r'(?<key>\w+):(?<value>\d+.\d+%)', value)
        key = match.group('key')
        value = match.group('value')
        key_values[key] = value

    return {"result": key_values}

def give_prediction(img: bytes):
    fp = io.BytesIO(img)
    with fp:
        new_image = plt.imread(fp, format="jpeg")
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
    return predicted_value

if __name__ == "__main__":
    uvicorn.run("server:app", reload=True)