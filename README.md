# Structured Extraction of Echocardiography Reports using DeepSeek-R1-Python

This project automates the structuring of unstructured **echocardiography reports** into key clinical variables using a Python script integrated with a **locally running Ollama language model**.

##  Objective

Extract specific, structured data fields from free-text echocardiography reports for further analysis or database entry.  
The fields extracted are:

###  Extracted Fields

1. **Enterprise Number**  
2. **Aortic Valve Mean Gradient (AVMG)**  
3. **Ejection Fraction (EF)**  
4. **TAVI Procedure** (Yes/No)  
5. **Execution Date** (Report date)

##  How It Works

**NOTE:** you must to install ollama model locally first

1. **Input:**  
   - Raw echocardiography report (free text, English or Arabic)
   - Optionally includes variable styles, abbreviations, and clinical phrasing

2. **Model Inference:**  
   - A prompt is sent to a locally running Ollama model (`DeepSeek-R1`)
   - The model parses and returns a structured JSON/dictionary with the target fields

3. **Output:**  
   - Clean tabular `.csv` or `.json` containing extracted data

##  Technology Stack

- **Ollama** (LLM runner) with model `DeepSeek-R1`
- **Python 3** for parsing, prompting, and structuring
- **Pandas** for saving and managing output
- **Local-first design**: everything runs offline for privacy

##  File Structure

```bash
├── echo_structuring.py       # Main script to process reports
├── reports/                  # Folder with raw echo reports (.txt)
├── structured_output.csv     # Final structured data output
├── ollama_config.json        # Optional config for prompts
```
 Example Prompt
{
  "instruction": "Extract the following fields from this echo report: Enterprise Number, AVMG, EF, TAVI procedure (Yes/No), and Execution Date.",
  "input": "Echo report for patient with enterprise number 45321. EF: 50%, AVMG 35 mmHg. TAVI was performed on 22-May-2023."
}
# Installation
Install dependencies:

```bash
pip install pandas requests
```
You must to add the medical reports in txt. file.

Start your Ollama model locally:
```bash
ollama run deepseek-r1:70b
```

# How to Use?
```bash
Add your .txt reports to the script instead of current file
```
Run the script:

```bash
python echo_structuring.py
```
Structured results will be saved to structured_output.csv
```
✅ Example Output:
1- Enterprise Number --> 00000
2-AVMG (mmHg) --> 35
3-EF (%)	--> 50
4- TAVI --> Yes
5- Execution Date --> 2023-05-22
```				

# Applications
EMR preprocessing

Clinical dashboard ingestion

Cardiovascular research datasets

Privacy-preserving clinical NLP

# License
MIT License

# Acknowledgements
Ollama for providing a lightweight local LLM interface

Medical domain experts for defining the extraction schema
