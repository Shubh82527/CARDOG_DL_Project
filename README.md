# 🐾 Pawprint - Cat vs Dog Image Classifier

A modern Deep Learning-powered web application that classifies images as **Cats 🐱** or **Dogs 🐶** using a Convolutional Neural Network (CNN) built with TensorFlow/Keras and deployed through Streamlit.

## 🌐 Live Demo

**Try the App:**
https://barnwal-sleepdisorderdl-map.streamlit.app/

## 📂 GitHub Repository

https://github.com/Shubh82527/Sleep_Disorder_DL

---

## 🚀 Project Overview

Pawprint is an end-to-end Deep Learning project that demonstrates the complete workflow of image classification:

* Dataset loading and preprocessing
* Image normalization
* CNN model development
* Model training and validation
* Performance evaluation
* Model saving and deployment
* Interactive Streamlit frontend

The application allows users to upload an image and instantly receive a prediction along with a confidence score.

---

## ✨ Features

✔ Upload JPG, JPEG, PNG, or WEBP images

✔ Real-time Cat vs Dog prediction

✔ Confidence score visualization

✔ Custom premium Streamlit UI

✔ Responsive design

✔ TensorFlow/Keras CNN model

✔ Fast inference

✔ Deployed and accessible online

---

## 🧠 Deep Learning Architecture

### CNN Architecture

Input Image (256×256×3)

↓

Conv2D (32 Filters) + ReLU

↓

MaxPooling2D

↓

Conv2D (64 Filters) + ReLU

↓

MaxPooling2D

↓

Conv2D (128 Filters) + ReLU

↓

MaxPooling2D

↓

Flatten

↓

Dense (128) + ReLU

↓

Dropout (0.1)

↓

Dense (64) + ReLU

↓

Dropout (0.1)

↓

Dense (1) + Sigmoid

↓

Prediction (Cat / Dog)

---

## 📊 Model Performance

| Metric        | Value               |
| ------------- | ------------------- |
| Test Accuracy | 78.42%              |
| Loss Function | Binary Crossentropy |
| Optimizer     | Adam                |
| Framework     | TensorFlow/Keras    |

---

## 🛠️ Tech Stack

### Machine Learning

* TensorFlow
* Keras
* NumPy

### Frontend

* Streamlit
* HTML
* CSS

### Image Processing

* Pillow (PIL)

### Deployment

* Streamlit Community Cloud

---

## 📁 Project Structure

```bash
Pawprint/
│
├── app.py
├── cat_dog_model.keras
├── requirements.txt
├── README.md
│
└── assets/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Shubh82527/Sleep_Disorder_DL.git

cd Sleep_Disorder_DL
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## 🖼️ How It Works

1. Upload an image.
2. Image is resized to 256×256.
3. Pixel values are normalized.
4. CNN processes the image.
5. Model predicts Cat or Dog.
6. Confidence score is displayed.

---

## 📚 Concepts Used

* Convolutional Neural Networks (CNN)
* Feature Extraction
* Max Pooling
* Flatten Layer
* Dense Layers
* Dropout Regularization
* Binary Classification
* Model Evaluation
* Streamlit Deployment

---

## 🎯 Future Improvements

* Multi-class pet classification
* Breed detection
* Grad-CAM visualization
* Mobile-friendly version
* Model performance optimization

---

## 👨‍💻 Author

**Shubh Barnwal**

B.Tech CSE Student | AI/ML Enthusiast

Building projects and documenting my AI/ML learning journey one day at a time.

---

## ⭐ Support

If you found this project useful, consider giving the repository a star ⭐.

It motivates me to build and share more AI/ML projects.


## Model File

The trained model file (`cat_dog_model.keras`) is not included in this repository because it exceeds GitHub's file size limit.

To generate the model:

1. Open the training notebook.
2. Run all cells.
3. Train the CNN model.
4. Save the model as:

```python
model.save("cat_dog_model.keras")
```

5. Place the generated file in the project root directory.

The Streamlit application will automatically load the model.
