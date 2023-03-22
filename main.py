import pyaudio
import speech_recognition as sr
from keras.models import load_model
from konlpy.tag import Komoran
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
import cv2
import numpy as np

model = load_model('./voice_phishing_model.h5')

r = sr.Recognizer()
mic = sr.Microphone()

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

cv2.namedWindow("Result", cv2.WINDOW_NORMAL)

tokenizer = Tokenizer()

def preprocess_text(text):
    kmr = Komoran()
    morphemes =kmr.morphs(text)
    return ' '.join(morphemes)

def predict_phishing(text):
    preprocessed_text = preprocess_text(text)
    sequence = tokenizer.texts_to_sequences([preprocessed_text])
    padded_sequence = pad_sequences(sequence, maxlen=50)
    predictions = model.predict(padded_sequence)
    phishing_probability = predictions[0][1]
    is_phishing = int(phishing_probability > 0.5)
    return is_phishing, phishing_probability

def predict_phishing(text):
    preprocessed_text = preprocess_text(text)
    sequence = tokenizer.texts_to_sequences([preprocessed_text])
    padded_sequence = pad_sequences(sequence, maxlen=50)
    predictions = model.predict(padded_sequence)
    phishing_probability = predictions[0][1]
    is_phishing = int(phishing_probability > 0.5)
    return is_phishing, phishing_probability

while True:
    with mic as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ko')
            print(f'Text: {text}')
            predict, prob = predict_phishing(text)
            if predict > 0.5:
                res_text = "CAUTION: High Chance of Voice Vishing"
            else:
                res_text = ""
            cv2.putText(img=np.zeros((200, 1000, 3), np.uint8), text=res_text, org=(50, 100),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
            cv2.imshow("Result", np.zeros(200, 1000, 3), np.uint8)
            cv2.waitKey(1)
        except sr.UnknownValueError:
            print("Cannot understand audio")
        except sr.RequestError as e:
            print("Cannot request results; {0}".format(e))