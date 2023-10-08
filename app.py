from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_text = request.form['userText']
    # Add your bot logic here to process user_text and get bot's response
    # For now, I'll just echo back the user's input
    return jsonify({'response': user_text})

if __name__ == '__main__':
    app.run(debug=True)
