from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os

app = Flask(__name__)
CORS(app)

# Set your Groq API key
# os.environ["GROQ_API_KEY"] = ''  # or set it securely via environment variables

llm = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key="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")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/handle_generate_blog', methods=['POST'])
def handle_generate_blog():
    """Generate a blog post based on the provided topic."""
    try:
        data = request.get_json()
        if not data or 'topic' not in data:
            return jsonify(error="Missing 'topic' in request"), 400
        
        if not isinstance(data['topic'], str) or not data['topic'].strip():
            return jsonify(error="Invalid input: 'topic' must be a non-empty string"), 400

        prompt = f"Generate a comprehensive blog post about: {data['topic']}. End the article with a separate line that says 'Hurray with a Space'."

        # Use Groq Chat model
        response = llm([HumanMessage(content=prompt)]).content

        return jsonify(content=response)

    except Exception as e:
        app.logger.error(f"Error generating blog: {str(e)}")
        return jsonify(error="Failed to generate blog"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# from flask import Flask, jsonify, request, render_template
# from flask_cors import CORS
# from langchain.llms import Ollama

# app = Flask(__name__)

# # Enable CORS for all routes
# CORS(app)

# # Initialize the Ollama model using Langchain
# llm = Ollama(model="deepseek-r1:1.5b")

# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/handle_generate_blog', methods=['POST'])
# def handle_generate_blog():
#     """Generate a blog post based on the provided topic."""
#     try:
#         # Get input data
#         data = request.get_json()
#         if not data or 'topic' not in data:
#             return jsonify(error="Missing 'topic' in request"), 400
        
#         # Validate the topic input
#         if not isinstance(data['topic'], str) or not data['topic'].strip():
#             return jsonify(error="Invalid input: 'topic' must be a non-empty string"), 400

#         # Generate content using the Ollama model through Langchain
#         prompt = f"Generate a comprehensive blog post about: {data['topic']} and finish the article with a separate line that says 'Hurray with a Space'"
#         response = llm(prompt)

#         return jsonify(content=response)

#     except Exception as e:
#         app.logger.error(f"Error generating blog: {str(e)}")
#         return jsonify(error="Failed to generate blog"), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
