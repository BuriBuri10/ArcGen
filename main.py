from flask import Flask, jsonify, render_template, request
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import ollama

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
