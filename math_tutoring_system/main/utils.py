import openai

# Set up your OpenAI API key
OPENAI_API_KEY = 'sk-Fex_R2ELJyqU5gHSE86wxScY6Qu2OpXMSXDkTIK3qpT3BlbkFJIrbtZUB71aYUi6wJ4ZV9xYH01s6qRCzNaWoMls6QAA'
openai.api_key = OPENAI_API_KEY

def check_solution(user_solution):
    try:
        # Use the OpenAI API to get feedback on the user solution
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model you're using
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_solution}
            ]
        )
        feedback = response['choices'][0]['message']['content']  # Access the feedback properly
        return feedback
    except Exception as e:
        return str(e)  # Return the error message if something goes wrong
