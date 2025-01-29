from flask import Flask, request, jsonify
import os
import tempfile
import fitz  # PyMuPDF
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure Google Generative AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def extract_text_from_pdf(pdf_file_path):
    text = ""
    with fitz.open(pdf_file_path) as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def analyze_text_with_gemini(text):
    chat_session = model.start_chat(history=[])
    prompt = f"Extract the name and email from the following text:\n\n{text}\n\nName and email:"
    response = chat_session.send_message(prompt)
    return response.text

def clean_response(response_text):
    lines = response_text.split("\n")
    name = None
    email = None

    for line in lines:
        if "Email:" in line:
            email = line.replace("Email:", "").strip()
        elif "Name:" in line:
            name = line.replace("Name:", "").strip()

    return name, email

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        # Extract text from PDF file
        resume_content = extract_text_from_pdf(temp_file_path)
        
        # Analyze text using Gemini API
        result = analyze_text_with_gemini(resume_content)
        
        # Clean and parse the result
        name, email = clean_response(result)
        
        if not email or not name:
            return jsonify({'error': 'Name and/or email not found in the resume'}), 404

        # Clean up temporary file
        os.remove(temp_file_path)

        return jsonify({'name': name, 'email': email})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
