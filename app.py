from flask import Flask, render_template, request, send_file
import database
import nlp_engine
import pdf_reader
import pdfgen as pdf_generator

app = Flask(__name__)

# ✅ Store results globally (for PDF download)
latest_results = []


# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')


# 📊 Analyze Contract
@app.route('/analyze', methods=['POST'])
def analyze():
    global latest_results

    text = request.form.get('contract')
    file = request.files.get('file')

    # 📄 If PDF uploaded
    if file and file.filename != "":
        text = pdf_reader.extract_text_from_pdf(file)

    # 🗄 Store contract
    contract_id = database.insert_contract(text)

    # 🔑 Get keywords
    keywords = database.get_keywords()

    # 🤖 NLP processing
    results = nlp_engine.analyze_contract(text, keywords)

    # ✅ Save for PDF
    latest_results = results

    # 💾 Store clauses
    for item in results:
        clause = item["clause"]
        risk = item["risk"]
        database.insert_clause(contract_id, clause, risk)

    # =========================
    # 📊 DASHBOARD CALCULATIONS
    # =========================

    high = sum(1 for r in results if r["risk"] == "High")
    medium = sum(1 for r in results if r["risk"] == "Medium")
    low = sum(1 for r in results if r["risk"] == "Low")

    total = len(results)

    # 🎯 AI Risk Score %
    overall_score = int((high*3 + medium*2 + low*1) / (total*3) * 100) if total > 0 else 0

    # 🧠 Auto Summary
    summary = f"This contract contains {high} high-risk clauses, {medium} medium-risk clauses, and {low} low-risk clauses. "

    if high > 0:
        summary += "There are critical risks related to penalties, termination, or liabilities."
    elif medium > 0:
        summary += "There are moderate risks that should be reviewed carefully."
    else:
        summary += "The contract appears mostly safe with minimal risks."

    # 📤 Send to UI
    return render_template(
        'result.html',
        results=results,
        high=high,
        medium=medium,
        low=low,
        overall_score=overall_score,
        summary=summary
    )


# 📥 Download PDF
@app.route('/download')
def download():
    global latest_results

    if not latest_results:
        return "No data available to generate PDF!"

    file_path = pdf_generator.generate_pdf(latest_results)
    return send_file(file_path, as_attachment=True)


# ▶ Run Server
if __name__ == '__main__':
    app.run(debug=True)