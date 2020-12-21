from PIL import Image
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from matplotlib.pyplot import imread

input_shape = (256,256)

def load_modal():
    model = load_model('potato.h5')
    return model

_model = load_modal()

def predict(image = Image):
    im = np.asarray(image)
    img_array = np.resize(im,(256,256,3))
    img_array = img_array * (1/255.0)
    img_array = np.expand_dims(img_array, axis=0)
    predictions = _model.predict(img_array)
    val0 = predictions[0][0].item() * 100
    val1 = predictions[0][1].item() * 100
    val2 = predictions[0][2].item() * 100
    val3 = predictions[0][3].item() * 100
    
    response = {
      'Potato Cut Worm':val0,
      'Early Blight':val1,
      'Late Blight':val2,
      'Healthy Potato':val3
      }
    return response


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image



