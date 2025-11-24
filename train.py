import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Load data
with open('data.json') as file:
    data = json.load(file)

texts, labels = [], []
for intent in data['intents']:
    for pattern in intent['patterns']:
        texts.append(pattern)
        labels.append(intent['tag'])

# Tokenize
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X, padding='post')
vocab_size = len(tokenizer.word_index) + 1

# Encode labels
encoder = LabelEncoder()
y = encoder.fit_transform(labels)

# Build model
model = Sequential([
    Embedding(vocab_size, 16, input_length=X.shape[1]),
    LSTM(16),
    Dense(16, activation='relu'),
    Dense(len(set(y)), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X, y, epochs=300)
model.save('chatbot_model.h5')
pickle.dump((tokenizer, encoder), open('tokenizer.pkl', 'wb'))

