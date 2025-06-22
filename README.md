# Structured-Extraction-of-Echocardiography-Reports-using-DeepSeek-R1-Python

This project automates the structuring of unstructured **echocardiography reports** into key clinical variables using a Python script integrated with a **locally running Ollama language model**.

## 🩺 Objective

Extract specific, structured data fields from free-text echocardiography reports for further analysis or database entry.  
The fields extracted are:

### 🔍 Extracted Fields

1. **Enterprise Number**  
2. **Aortic Valve Mean Gradient (AVMG)**  
3. **Ejection Fraction (EF)**  
4. **TAVI Procedure** (Yes/No)  
5. **Execution Date** (Report date)

## ⚙️ How It Works

1. **Input:**  
   - Raw echocardiography report (free text, English or Arabic)
   - Optionally includes variable styles, abbreviations, and clinical phrasing

2. **Model Inference:**  
   - A prompt is sent to a locally running Ollama model (e.g., `llama3`)
   - The model parses and returns a structured JSON/dictionary with the target fields

3. **Output:**  
   - Clean tabular `.csv` or `.json` containing extracted data

## 🧠 Technology Stack

- **Ollama** (LLM runner) with model `DeepSeek-R1`
- **Python 3** for parsing, prompting, and structuring
- **Pandas** for saving and managing output
- **Local-first design**: everything runs offline for privacy

## 🗂 File Structure

```bash
├── echo_structuring.py       # Main script to process reports
├── reports/                  # Folder with raw echo reports (.txt)
├── structured_output.csv     # Final structured data output
├── ollama_config.json        # Optional config for prompts
```
💡 Example Prompt
json
Copy
Edit
{
  "instruction": "Extract the following fields from this echo report: Enterprise Number, AVMG, EF, TAVI procedure (Yes/No), and Execution Date.",
  "input": "Echo report for patient with enterprise number 45321. EF: 50%, AVMG 35 mmHg. TAVI was performed on 22-May-2023."
}
📦 Installation
Install dependencies:

```bash
Copy
Edit
pip install pandas requests
Start your Ollama model locally:
```
```bash
Copy
Edit
ollama run llama3
🚀 How to Use
Add your .txt reports to the reports/ folder
```
Run the script:

```bash
Copy
Edit
python echo_structuring.py
Structured results will be saved to structured_output.csv
```
✅ Example Output
Enterprise Number	AVMG (mmHg)	EF (%)	TAVI	Execution Date
45321	35	50	Yes	2023-05-22

📌 Applications
EMR preprocessing

Clinical dashboard ingestion

Cardiovascular research datasets

Privacy-preserving clinical NLP

📜 License
MIT License

🙏 Acknowledgements
Ollama for providing a lightweight local LLM interface

Medical domain experts for defining the extraction schema
