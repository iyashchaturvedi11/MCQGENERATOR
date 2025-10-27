# MCQ Generator 🎯

An intelligent MCQ (Multiple Choice Question) generator powered by Google's Gemini AI. Upload your documents and automatically generate multiple-choice questions.

## Features ✨

- 📄 Support for multiple file formats (PDF, TXT, DOCX)
- 🤖 Powered by Google Gemini AI for intelligent question generation
- 📑 Export generated questions as TXT and PDF
- 🎨 Beautiful, modern UI with responsive design
- ⚡ Fast and efficient processing

## Installation 📦

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google API Key:**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - The key is already configured in `main.py` (line 11)
   - Or set it as an environment variable:
     ```bash
     set GOOGLE_API_KEY=your_api_key_here
     ```

## Usage 🚀

1. **Run the Flask application:**
   ```bash
   python main.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Upload your document** (PDF, TXT, or DOCX format)

4. **Specify the number of questions** you want to generate

5. **Click "Generate MCQs"** and wait for the results

6. **Download** your questions as TXT or PDF

## Project Structure 📁

```
mcq-generator/
├── main.py                 # Flask backend application
├── templates/              # HTML templates
│   ├── index.html         # Upload page
│   └── results.html       # Results display page
├── uploads/               # Uploaded files storage
├── results/               # Generated output files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Supported File Formats 📄

- **PDF** - Extract text from PDF documents
- **TXT** - Plain text files
- **DOCX** - Microsoft Word documents

## Technologies Used 🛠️

- **Backend:** Flask (Python web framework)
- **AI:** Google Gemini 1.5 Pro
- **PDF Processing:** pdfplumber
- **Document Processing:** python-docx
- **PDF Generation:** fpdf
- **Frontend:** HTML5, CSS3 with modern design

## Notes 📝

- Make sure you have a valid Google API key
- The API key in the code is for demonstration purposes
- Generated files are stored in the `results/` folder
- Uploaded files are stored in the `uploads/` folder

## License 📄

This project is open source and available for educational purposes.

## Troubleshooting 🔧

If you encounter any issues:

1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Check that your Google API key is valid
3. Ensure the uploads and results folders exist
4. Verify your file format is supported (PDF, TXT, DOCX)

---

Made with ❤️ using Flask and Google Gemini AI
