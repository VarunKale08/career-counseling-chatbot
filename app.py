from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
import joblib

app = Flask(__name__)

# Load the trained SVM model
svm_model = joblib.load('career_counseling_model.joblib')

# Function to preprocess the data
def preprocess_data(df):
    df.columns = df.columns.str.strip()
    scaler = MinMaxScaler()
    numerical_columns = ['Mathematics', 'Science', 'Social_Studies', 'English']
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    return df

# Function to get career suggestion
def get_career_suggestion(user_input):
    user_input = preprocess_data(user_input)
    prediction = svm_model.predict(user_input)
    return prediction[0]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_text = request.form['userText']
    # Add your bot logic here to process user_text and get bot's response
    # For now, I'll just echo back the user's input
    return jsonify({'response': user_text})

@app.route('/webhook', methods=['POST'])
def webhook():
    user_input = request.json  # Assuming it contains user's input
    interested_field = get_career_suggestion(user_input)
    return jsonify({'interested_field': interested_field})

if __name__ == '__main__':
    app.run(debug=True)
