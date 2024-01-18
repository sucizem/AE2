#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from flask import Flask, request
import gensim

app = Flask(__name__)

# Load trained Word2Vec model
model = gensim.models.Word2Vec.load("model_su") #can exchange for model_su_no_stop
reference_pair = ("full", "empty")  # Reference words used in finding opposites

# HTML template for the front-end interface
html_form_with_message = '''
<!DOCTYPE html>
<html>
<head>
<title>Opposite Word Finder</title>
</head>
<body>
    <h2>Find the Opposite of a Word</h2>
    <h3>Enter a word and see its opposite (e.g., hot, fast, day)</h3>
    <form method="post" action="/">
        <label for="text">Enter Word:</label><br>
        <input type="text" name="my_input_value" required><br><br>
        <input type="submit" value="Find Opposite">
    </form>
    <style>
        body {
            background-color: lightblue;
            font-family: Arial, sans-serif;
        }
    </style>
    <p>Opposite Word: DATA</p>
</body>
</html>
'''

# calculate the opposite word
def calculate_opposite(target_word):
    try:
        if target_word in model.wv:    
            result_vector = model.wv[target_word] - model.wv[reference_pair[0]] + model.wv[reference_pair[1]]
            opposite_word = model.wv.similar_by_vector(result_vector, topn=1)[0][0]
            return opposite_word
        else:
            return "Word not found in model"
    except Exception as e:
        # Return error 
        return "Error: " + str(e)

# Define the route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    display_text = "Enter a word above"
    if request.method == 'POST':
        user_input = request.form['my_input_value'].lower()
        display_text = calculate_opposite(user_input)
    return html_form_with_message.replace("DATA", display_text)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

