from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/handle_generate_blog', methods=['POST'])
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
            prompt=f"Generate a comprehensive blog post about: {data['topic']} and finish the article with a seprate line that says 'Hurray with a Space'",
            options={
                'temperature': 0.7,
                'num_predict': 5000  # Ollama uses 'num_predict' instead of 'max_tokens'
            }
        )
        
        return jsonify(content=response['response'])
    
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
