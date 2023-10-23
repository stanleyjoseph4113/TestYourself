from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Replace 'your_api_key_here' with your actual OpenAI API key
api_key = "api_key"

# Initialize the OpenAI API client
openai.api_key = api_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    try:
        topic = request.form.get('topic')
        num_questions = 3  # Adjust the number of questions as needed
        question_type = request.form.get('questionType')  # Get the selected question type

        # Customize the user message based on the selected question type
        if question_type == 'mcq':
            user_message = [
                {"role": "system", "content": f"Generate {num_questions} multiple-choice questions about {topic}."},
                {"role": "user", "content": ""}
            ]
        elif question_type == 'descriptive':
            user_message = [
                {"role": "system", "content": f"Generate {num_questions} descriptive questions about {topic}."},
                {"role": "user", "content": ""}
            ]
        else:
            return jsonify({'error': 'Invalid question type'})

        # Call the OpenAI API to generate questions
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Replace with your desired GPT model
            messages=user_message,
            max_tokens=500  # Set the maximum number of tokens for the response here
        )

        if response['object'] == 'chat.completion':
            assistant_responses = response['choices'][0]['message']['content'].split("\n")
            questions = [q.strip() for q in assistant_responses if q.strip()]

            formatted_questions = []
            if question_type == 'mcq':
                # Format MCQs with options A, B, C, and D
                for i, question in enumerate(questions[:num_questions]):
                    options = ["A", "B", "C", "D"]
                    formatted_question = f"Question {i + 1}: {question}"
                    for j, option in enumerate(options):
                        formatted_question += f"\n{option}. [Option {j + 1}]"
                    formatted_questions.append(formatted_question)
            else:
                # For descriptive questions, simply display the questions
                formatted_questions = questions[:num_questions]

            return jsonify({'questions': formatted_questions})
        else:
            return jsonify({'error': 'Failed to generate questions'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
