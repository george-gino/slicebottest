from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="sk-proj-qD9B9OzLxk3ZcKZ3fHM4T3BlbkFJBxz9ZyxAWj0f2JKUayEd")

def get_additional_data(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Adjust the path to your actual text file
additional_data = get_additional_data('data.txt')

def get_response_with_data(prompt):
    try:
        full_prompt = f"{additional_data}\n\n{prompt}"
        response = client.chat.completions.create(model="gpt-4-turbo",  # Use the latest model
                                                  messages=[{"role": "system",
                                                             "content": "You are a real estate broker that helps customers find commercial real estate spaces. You will read in additional data that contains all the possible locations" +
                                                                        "Some of the requirements you need are location, minimum and max number of people and the cost per head. THe requiremments are IMPORTANT do not give recommendations that do not fit, if there are none say there are none dont do any calculations in front of the user"},
                                                            {"role": "user", "content": full_prompt}],
                                                  max_tokens=100)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error processing your request."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = get_response_with_data(user_input)
        return render_template('index.html', user_input=user_input, response=response)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)








