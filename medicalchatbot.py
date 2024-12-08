from flask import Flask, request, jsonify, render_template
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import json
import pickle
import random

app = Flask(_name_)

stemmer = LancasterStemmer()

with open('intents.json') as f:
    data = json.load(f)

with open('data.pickle', 'rb') as f:
    words, labels, training, output = pickle.load(f)

tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.load("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    if not message:
        return jsonify({"error": "Invalid input"}), 400
    if message.lower() == "quit":
        return jsonify({"response": "Goodbye! Have a great day!"})

    results = model.predict([bag_of_words(message, words)])
    results_index = np.argmax(results)
    tag = labels[results_index]
    
    
    for tg in data['intents']:
        if tg['tag'] == tag:
            responses = tg['responses']
            return jsonify({"response": random.choice(responses)})

    return jsonify({"response": "I don't understand!"})

if _name_ == '_main_':
    app.run(debug=True)