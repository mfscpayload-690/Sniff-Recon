# 📘 Sniff-Recon Documentation

## 🧠 Overview

**Sniff-Recon** is an AI-powered network log analyzer that processes and summarizes `.pcap`, `.pcapng`, and other network capture logs. Built for cybersecurity enthusiasts, it leverages Google’s Pegasus model (via Hugging Face) to identify anomalies, summarize packet activity, and assist in network forensics.

---

## 🎯 Objectives

* Analyze `.pcap`/`.pcapng` files with AI support
* Summarize traffic using natural language
* Extract top IPs, ports, and protocols
* Provide a chat interface to ask traffic-related questions
* Offer a GUI for easier interaction

---

## 🧰 Technology Stack

| Component     | Tool/Library                               |
| ------------- | ------------------------------------------ |
| Language      | Python 3.x                                 |
| AI Model      | Pegasus via Hugging Face                   |
| Packet Parser | PyShark (based on tshark)                  |
| GUI           | Streamlit                                  |
| Visualization | Matplotlib / Plotly                        |
| Env Variables | Python-dotenv                              |
| File Support  | `.pcap`, `.pcapng`, `.log`, `.txt`, `.csv` |

---

## 🛠️ Features

### 🔍 PCAP Log Parsing

* Parse `.pcap`/`.pcapng` with PyShark
* Extract key insights: protocols, flows, IPs

### 🧠 AI Summarization

* Uses Pegasus (CNN/DailyMail) to summarize human-readable traffic logs
* Detects possible threats or abnormal patterns

### 💬 Chat-Like Queries

* Ask questions like:

  * "Show top IPs in this capture"
  * "What kind of DNS activity is present?"

### 📈 Visual Analysis

* Graphs and charts for:

  * Top source/destination IPs
  * Protocol usage
  * Traffic timelines

---

## 📂 Project Structure

```
sniff-recon/
├── src/
│   ├── parsers/         # PCAP parsing & traffic extraction
│   ├── ai/              # AI summarization using Pegasus
│   ├── ui/              # Streamlit-based frontend
├── config/              # Config & keys
├── .env                 # Hugging Face API Token
├── requirements.txt     # Python dependencies
└── main.py              # App entry point
```

---

## 🔐 Setup Instructions

1. Clone the repo:

   ```bash
   git clone https://github.com/YOUR_USERNAME/Sniff-Recon.git
   cd Sniff-Recon
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add Hugging Face API token to `.env`:

   ```env
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxx
   ```

4. Run the app:

   ```bash
   streamlit run main.py
   ```

---

## 📜 License

Licensed under the **MIT License**.
Free for personal and academic use. Attribution required.

---

## 👨‍💻 Author

Made with ❤️ by **Aravind Lal**
Cybersecurity + Python + AI = 💥
