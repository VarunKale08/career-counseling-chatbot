from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    intent = data['queryResult']['intent']['displayName']
    
    if intent == 'GetCareerSuggestion':
        # Assuming you want to get a career suggestion from the user's input
        user_text = data['queryResult']['queryText']
        response = get_career_suggestion(user_text)
    else:
        response = "I'm sorry, I don't understand that."

    reply = {'fulfillmentText': response}
    return jsonify(reply)

def get_career_suggestion(user_input):
    # Add your logic to process user input and get career suggestion here
    # For now, let's assume a basic response
    return "Based on your input, I suggest exploring careers in the field of Science."

if __name__ == '__main__':
    app.run(debug=True)

