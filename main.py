import os
from flask import Flask, render_template, request, send_file
import pdfplumber
import docx
import csv
from werkzeug.utils import secure_filename
import google.generativeai as genai
from fpdf import FPDF


os.environ["GOOGLE_API_KEY"] = "AIzaSyAB_c2GTSiyccbiquUXfhbv1JlnU_MnA3k"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


model = genai.GenerativeModel('gemini-2.0-flash')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
MAX_TEXT_LENGTH = 100000
MAX_PAGES_PROCESS = 300

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_file(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    text = ""
    
    if ext == 'pdf':
        try:
            with pdfplumber.open(file_path) as pdf:

                for i, page in enumerate(pdf.pages):
                    if i >= MAX_PAGES_PROCESS or len(text) > MAX_TEXT_LENGTH:
                        break
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
            
    elif ext == 'docx':
        try:
            doc = docx.Document(file_path)
            text = ' '.join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
            
    elif ext == 'txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                text = file.read()
        except Exception as e:
            return f"Error reading TXT: {str(e)}"
    

    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH] + "\n\n[Text truncated due to length...]"
    
    return text.strip()

def Question_mcqs_generator(input_text, num_questions):
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
    Please generate {num_questions} MCQs from the text. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """
    response = model.generate_content(prompt).text.strip()
    return response

def save_mcqs_to_file(mcqs, filename):
    results_path = os.path.join(app.config['RESULTS_FOLDER'], filename)

    with open(results_path, 'w', encoding='utf-8') as f:
        f.write(mcqs)
    return results_path

def create_pdf(mcqs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            pdf.multi_cell(0, 10, mcq.strip())
            pdf.ln(5)

    pdf_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    pdf.output(pdf_path)
    return pdf_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_mcqs():
    try:
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)


            file_size = os.path.getsize(file_path)
            if file_size > 200 * 1024 * 1024:  # 200MB limit
                return f"File too large ({file_size / (1024*1024):.2f}MB). Please upload a file smaller than 200MB."


            text = extract_text_from_file(file_path)

            if text:
                if not text.strip():
                    return "Could not extract text from the file. Please ensure the file contains readable text."
                    
                num_questions = int(request.form['num_questions'])
                

                print(f"Processing {filename} ({len(text)} characters)...")
                
                try:
                    mcqs = Question_mcqs_generator(text, num_questions)


                    txt_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.txt"
                    pdf_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.pdf"
                    save_mcqs_to_file(mcqs, txt_filename)
                    create_pdf(mcqs, pdf_filename)


                    return render_template('results.html', mcqs=mcqs, txt_filename=txt_filename, pdf_filename=pdf_filename)
                except Exception as e:
                    return f"Error generating MCQs: {str(e)}. Please try again with fewer questions or a smaller document."
            else:
                return "Could not extract text from the file."
        return "Invalid file format"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['RESULTS_FOLDER']):
        os.makedirs(app.config['RESULTS_FOLDER'])
    app.run(debug=True)