import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import Counter



    ###### pre-processing image i.e resizing and converting into grey scale

def preprocess_image(image):
    image = cv2.resize(image, (28, 28)) # Resize the image to 28x28    
    
    if len(image.shape) == 3:       # Convert to grayscale if it isn't already
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    image = image.astype('float32') / 255.0 # Normalize the image to the range [0, 1]
    
    image = np.expand_dims(image, axis=-1)   # Expand dimensions to match the input shape (28, 28, 1)
    
    image = np.expand_dims(image, axis=0)   # Expand dimensions to match the batch size (1, 28, 28, 1)
    return image




                #### loading pre-trained models ######
                                
model1 = load_model('saved_models/model1_saved.h5')
model2 = load_model('saved_models/model2_saved.h5')
model3 = load_model('saved_models/model3_saved.h5')
model4 = load_model('saved_models/model4_saved.h5')
model5 = load_model('saved_models/model5_saved.h5')
model6 = load_model('saved_models/model6_saved.h5')


def predict_letter(image):

    image = preprocess_image(image)
    
    # Predict the letter using the model
    prediction1=model1.predict(image)
    prediction2=model2.predict(image)
    prediction3=model3.predict(image)
    prediction4=model4.predict(image)
    prediction5=model5.predict(image)
    prediction6=model6.predict(image)

    # Get the index of the highest probability
    predicted_letter_index1 = np.argmax(prediction1)
    predicted_letter_index2 = np.argmax(prediction2)
    predicted_letter_index3 = np.argmax(prediction3)
    predicted_letter_index4 = np.argmax(prediction4)
    predicted_letter_index5 = np.argmax(prediction5)
    predicted_letter_index6 = np.argmax(prediction6)
    
    
    vote=[predicted_letter_index1,predicted_letter_index2,predicted_letter_index3,predicted_letter_index4,predicted_letter_index5,predicted_letter_index6]
    vote_counts = Counter(vote)
    most_common_value, count = vote_counts.most_common(1)[0]
    return most_common_value