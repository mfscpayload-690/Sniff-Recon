# 🕵️‍♂️ Sniff Recon - Network Log Analyzer

Sniff Recon is a powerful Python-based tool designed to analyze network packet capture (PCAP/PCAPNG) files, CSV exports, and text-based logs. It offers both a user-friendly GUI (via Streamlit) and a CLI interface, making it versatile for both beginners and experienced cybersecurity professionals. Built for log management, packet inspection, intrusion detection, and natural language queries, Sniff Recon helps you gain actionable insights from raw packet data.

---

<img width="1003" height="1052" alt="image" src="https://github.com/user-attachments/assets/f3bd1893-900a-42aa-8b3b-61b1e439149c" />


## 🚀 Features

### ✅ Core Capabilities

- 📂 Upload and analyze `.pcap`, `.pcapng`, `.csv`, or `.txt` network logs
- 📊 Real-time summary report including:
  - Total packets
  - Unique source & destination IPs
  - Top talkers (IP frequency)
  - Protocol distribution (TCP/UDP/etc)

### 🔍 Lightweight AI-powered Natural Language Querying

Ask questions like:

- "What are the top 5 source IPs?"
- "Count HTTPS GET requests"
- "List suspected intrusions"

### 🧠 AI Summary Engine

- Summarizes packet data into a human-readable format
- Highlights anomalies, suspicious patterns, and traffic spikes

### 🌐 Full HTML Report

Generates and opens a styled browser-based report summarizing:

- Timeline
- Protocols used
- IP frequency heatmap
- Intrusion markers

### 🧑‍💻 Dual Mode Interface

- CLI for minimalists and scripting
- GUI for streamlined exploration (built with Streamlit)

---

## 📁 Project Structure

```
Sniff-Recon/
├── assets/                # Images, icons, and UI assets
├── core/
│   ├── parser.py          # Parses PCAP, CSV, TXT into DataFrames
│   ├── analyzer.py        # Generates summaries and protocol stats
│   └── ai_module.py       # Handles natural language queries
├── cli.py                 # Command-line interface script
├── app.py                 # Streamlit GUI app
├── utils.py               # Helper functions
├── requirements.txt       # Dependencies
├── report_template.html   # HTML template for log report
└── README.md
```

---

## 🛠️ Installation & Usage

### 🔹 1. Clone the Repo

```bash
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon
```

### 🔹 2. Setup Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 🔹 3. Run GUI (Streamlit)

```bash
streamlit run app.py
```

### 🔹 4. Run CLI Tool

```bash
python cli.py <path-to-pcap-or-csv-file>
```

---

## 🧠 Example AI Query Outputs

> **What are the top 5 destination IPs?**  
> `{'10.48.167.21': 93, '23.212.254.65': 40, ...}`

> **Count HTTPS GET requests**  
> Output: 62 GET requests using TCP Port 443

> **Detect intrusions**  
> Output: No obvious port scan or SYN flood patterns detected.

---

## 🪪 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute!

---

## 👨‍💻 Author

Aravind Lal  
💻 [GitHub](https://github.com/mfscpayload-690) | 📫 [LinkedIn](https://www.linkedin.com/in/aravind-lal)

> "Logs don't lie—if you know how to read them."
