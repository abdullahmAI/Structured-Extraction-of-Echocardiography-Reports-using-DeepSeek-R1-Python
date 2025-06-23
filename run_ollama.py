import requests
import json
import csv
import os
import re

# -----------------------------------------------
# CONFIGURATION
# -----------------------------------------------
OLLAMA_MODEL = "deepseek-r1:70b"  # Change to smaller model if needed (e.g. "mistral")
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama serve endpoint

INPUT_FILE = "/home/deep/Desktop/Abdullah/medical"
OUTPUT_CSV = "structured_medical_data.csv"

# -----------------------------------------------
# CSV SETUP
# -----------------------------------------------
if not os.path.exists(OUTPUT_CSV):
    with open(OUTPUT_CSV, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Enterprise Number", 
            "MPG (mmHg)", 
            "ASPG (mmHg)", 
            "Transvalvular Mean Gradient (mmHg)", 
            "Ejection Fraction (EF) (%)", 
            "TAVI (Yes/No)"
        ])

# -----------------------------------------------
# REGEX EXTRACTION FUNCTION
# -----------------------------------------------
def extract_value(text, pattern, default="N/A"):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else default

# -----------------------------------------------
# OLLAMA PARSE FUNCTION
# -----------------------------------------------
def parse_report_with_ollama(report):
    """
    Sends the report to Ollama via HTTP API and
    instructs it to output structured data only.
    """
    
    # >> Prompt: Force Ollama to output strict format
    prompt = f"""
    You are a medical data extraction assistant.
    Given this single patient report, extract:

    1) Enterprise Number: (7 digits)
    2) Mean Pressure Gradient (MPG) [mmHg]
    3) Aortic Stenosis Peak Gradient (ASPG) [mmHg]
    4) Transvalvular Mean Gradient [mmHg]
    5) Ejection Fraction (EF) [%]
    6) TAVI (Yes/No)

    If a value is missing, output N/A.
    The output must strictly follow:

    Enterprise Number: XXXXXXX
    MPG: XX mmHg
    ASPG: XX mmHg
    Transvalvular Mean Gradient: XX mmHg
    Ejection Fraction (EF): XX%
    TAVI: Yes/No or N/A
    
    Report:
    {report}
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt.strip(),
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_API_URL, json=payload)
        r.raise_for_status()
        data = r.json()
        
        if "response" not in data:
            print("❌ No valid 'response' key in Ollama's output.")
            return None

        response_text = data["response"]
        # Example: 
        # Enterprise Number: 1234567
        # MPG: 6.1 mmHg
        # ASPG: N/A mmHg
        # Transvalvular Mean Gradient: 6.1 mmHg
        # Ejection Fraction (EF): 66%
        # TAVI: N/A

        # >> Extract fields with regex
        enterprise_number = extract_value(
            response_text, 
            r"Enterprise Number.*?:\s*(\d{7})", 
            default="Unknown"
        )
        mpg = extract_value(
            response_text, 
            r"MPG.*?:\s*([\d\.>]+)\s*mmHg", 
            default="N/A"
        )
        aspg = extract_value(
            response_text, 
            r"ASPG.*?:\s*([\d\.>]+)\s*mmHg", 
            default="N/A"
        )
        transvalvular = extract_value(
            response_text, 
            r"Transvalvular Mean Gradient.*?:\s*([\d\.>]+)\s*mmHg", 
            default="N/A"
        )
        ef = extract_value(
            response_text, 
            r"Ejection Fraction \(EF\).*?:\s*([\d\.>]+)%", 
            default="N/A"
        )
        tavi = extract_value(
            response_text, 
            r"TAVI.*?:\s*(Yes|No|N/A)", 
            default="No"
        )

        return [enterprise_number, mpg, aspg, transvalvular, ef, tavi]

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return None

# -----------------------------------------------
# MAIN LOOP: READ FILE, PARSE, WRITE CSV
# -----------------------------------------------
def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ {INPUT_FILE} not found. Please create it first.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    print(f"🚀 Found {len(lines)} lines (reports). Processing...")

    # Loop each line (1 line = 1 report with 7-digit ID at start)
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 1) Check that line starts with a 7-digit ID
        match_id = re.match(r"^(\d{7})", line)
        if not match_id:
            # If not found, we can skip or try a fallback
            print(f"⚠️ Skipping line (no 7-digit ID found): {line[:50]}")
            continue

        structured_data = parse_report_with_ollama(line)
        if structured_data:
            with open(OUTPUT_CSV, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(structured_data)
        else:
            print("⚠️ No structured data returned.")

    print(f"✅ All reports processed. See '{OUTPUT_CSV}' for results.")

if __name__ == "__main__":
    main()
