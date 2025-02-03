from flask import Flask, jsonify, render_template, request
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
import ollama

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate_blog', methods=['POST'])  # Only allow POST for this route

@app.route('/generate_blog', methods=['POST'])
def handle_generate_blog():
    """Handle blog generation requests"""
    try:
        # Get input data
        data = request.get_json()
        if not data or 'topic' not in data:
            return jsonify(error="Missing 'topic' in request"), 400
            
        # Generate content
        response = ollama.generate(
            model="deepseek-r1:1.5b",
            prompt=f"Generate a comprehensive blog post about: {data['topic']}",
            options={
                'temperature': 0.7,
                'num_predict': 500  # Ollama uses 'num_predict' instead of 'max_tokens'
            }
        )
        
        return jsonify(content=response['response'])
    
    except Exception as e:
        app.logger.error(f"Error generating blog: {str(e)}")
        return jsonify(error="Failed to generate blog"), 500

# def generate():
#     # Get the prompt from the request
#     user_input = request.get_json().get('text')  # Ensure the key matches what you send from the client
#     print(f"Received prompt: {user_input}")  # Debugging output

#     # Create a prompt template
#     prompt_template = PromptTemplate.from_template('Generate a blog on the topic: {text}')

#     # Initialize the language model
#     llm = OpenAI(temperature=0.9, api_key=OPENAI_API_KEY)

#     # Create a chain with the language model and the prompt
#     chain = LLMChain(llm=llm, prompt=prompt_template)

#     try:
#         # Run the chain with the user input
#         output = chain.run(text=user_input)  # Pass the user input as 'text'
#         return jsonify(output=output)  # Return the output as JSON
#     except Exception as e:
#         print(f"Error generating output: {e}")  # Log the error
#         return jsonify(error="An error occurred while generating the article."), 500  # Return an error response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)