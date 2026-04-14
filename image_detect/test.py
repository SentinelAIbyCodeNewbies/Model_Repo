import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
import matplotlib.pyplot as plt


saved_model = load_model('xception_deepfake_base.keras')

def manual_test_xception(model, img_path):
  print(f"Loading image: {img_path}")

  img = image.load_img(img_path, target_size=(224, 224))

  img_array = image.img_to_array(img)

  img_array = np.expand_dims(img_array, axis=0)

  img_array = preprocess_input(img_array)

  prediction_score = model.predict(img_array)[0][0]

  if prediction_score >= 0.5:
    label = "Real"
    confidence = prediction_score * 100
  else:
    label = "Fake"
    confidence = (1.0 - prediction_score) * 100

  print(f"Raw Model Score: {prediction_score:.4f}")
  print(f"Prediction: {label} (Confidence: {confidence:.2f}%)")

  plt.imshow(img)
  plt.title(f"{label} ({confidence:.1f}%)")
  plt.axis('off')
  plt.show()

img_path = input("Enter the path to the image you want to test: ")

manual_test_xception(saved_model, img_path)