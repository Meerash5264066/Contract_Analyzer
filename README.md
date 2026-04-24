# Contract Risk Analyzer

Contract Risk Analyzer is an AI-powered web application built with Flask that helps users automatically analyze legal contracts for potential risks. It extracts text from uploaded PDFs or raw text inputs, evaluates clauses based on risk keywords using Natural Language Processing (NLP), and categorizes them into High, Medium, and Low risk levels. 

The application provides a user-friendly dashboard with risk summaries, an overall risk score, and the ability to download a comprehensive PDF report.

## Features

- **Upload & Parse PDFs:** Easily extract text from contract PDF documents.
- **Direct Text Analysis:** Paste contract text directly for quick analysis.
- **Risk Assessment:** Automatically identifies and categorizes clauses into High, Medium, or Low risk based on predefined keyword analysis.
- **Smart Dashboard:** Visualizes risk levels, calculates an overall AI risk score, and provides an auto-generated summary of the contract.
- **PDF Report Generation:** Download a structured PDF report containing the detailed risk analysis of the contract.
- **Database Storage:** Contracts and analyzed clauses are stored securely in a local database for tracking.

## Technology Stack

- **Backend:** Python, Flask
- **NLP / Processing:** Custom NLP Engine (`nlp_engine.py`)
- **PDF Processing:** PyPDF2/pdfminer (via `pdf_reader.py`), ReportLab (via `pdfgen.py` for generation)
- **Frontend:** HTML, CSS
- **Database:** SQLite (via `database.py`)

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Meerash5264066/Contract_Analyzer.git
   cd Contract_Analyzer
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   Make sure you have the required Python libraries installed (Flask, reportlab, etc.). If a `requirements.txt` is available, run:
   ```bash
   pip install -r requirements.txt
   ```
   *(If not, manually install: `pip install flask reportlab PyPDF2`)*

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the web app:**
   Open your browser and navigate to `http://127.0.0.1:5000/`

## Usage

1. Open the homepage.
2. Paste the contract text into the provided text area or upload a PDF document.
3. Click on the "Analyze" button.
4. Review the generated risk dashboard, including the risk breakdown, overall score, and categorized clauses.
5. Click "Download PDF Report" to save a copy of the results.

## Project Structure

- `app.py`: Main Flask application handling routing and application logic.
- `database.py`: Handles SQLite database operations (storing contracts, clauses, keywords).
- `nlp_engine.py`: Core logic for parsing contract text and assigning risk levels based on keywords.
- `pdf_reader.py`: Utility to extract text from uploaded PDF files.
- `pdfgen.py`: Utility to generate downloadable PDF reports from analysis results.
- `templates/`: Contains HTML templates (`index.html`, `result.html`).
- `static/`: Contains static assets like CSS (`static/css/style.css`).
- `test_nlp.py` / `python_test_db.py`: Scripts for testing NLP and database functionality.
