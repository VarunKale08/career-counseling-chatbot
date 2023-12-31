from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
import requests

app = Flask(__name__)

# Load the trained SVM model
svm_model = joblib.load('career_counseling_model.joblib')

# Load your dataset
# Assuming your dataset is in CSV format
dataset = pd.read_csv('dataset.csv')  # Updated file name

# Function to preprocess the data
def preprocess_data(df):
    df.columns = df.columns.str.strip()
    scaler = MinMaxScaler()
    numerical_columns = ['Mathematics', 'Science', 'Social_Studies', 'English']
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    return df

def get_career_suggestion(maths, science, social_studies, english):
    user_input = pd.DataFrame({
        'Mathematics': [maths],
        'Science': [science],
        'Social_Studies': [social_studies],
        'English': [english]
    })
    user_input = preprocess_data(user_input)
    prediction = svm_model.predict(user_input)
    return prediction[0]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_text = request.form['userText']
    
    # Assuming you want to call the Dialogflow webhook here
    dialogflow_response = get_dialogflow_response(user_text)
    
    return jsonify({'response': dialogflow_response})

def get_dialogflow_response(user_text):
    # Assuming your Dialogflow webhook URL is 'https://career-counseling-app.azurewebsites.net/webhook'
    dialogflow_url = 'https://career-counseling-app.azurewebsites.net/webhook'
    
    data = {
        'queryResult': {
            'intent': {
                'displayName': 'GetCareerSuggestion'
            },
            'queryText': user_text
        }
    }
    
    response = requests.post(dialogflow_url, json=data)
    return response.json()['fulfillmentText']

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req['queryResult']['intent']['displayName']
    
    if intent == 'CareerGuidanceIntent':
        marks_in_maths = req['queryResult']['parameters']['marks_in_maths']
        marks_in_science = req['queryResult']['parameters']['marks_in_science']
        marks_in_social_studies = req['queryResult']['parameters']['marks_in_social_studies']
        marks_in_english = req['queryResult']['parameters']['marks_in_english']
        
        suggestion = get_career_suggestion(marks_in_maths, marks_in_science, marks_in_social_studies, marks_in_english)
        
        response = {
            'fulfillmentText': f'Based on your marks, I suggest exploring careers in the field of {suggestion}.'
        }
    else:
        response = {
            'fulfillmentText': 'I\'m sorry, I don\'t understand that.'
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
