import argparse
import os
import sys
from parsers import pcap_parser, csv_parser, txt_parser
import json

def detect_file_type(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    if ext in ['.pcap', '.pcapng']:
        return 'pcap'
    elif ext == '.csv':
        return 'csv'
    elif ext == '.txt':
        return 'txt'
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description='Sniff Recon - Network Log Analyzer')
    parser.add_argument('file', help='Path to the network log file (.pcap, .pcapng, .csv, .txt)')
    args = parser.parse_args()

    file_path = args.file
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    file_type = detect_file_type(file_path)
    if not file_type:
        print(f"Error: Unsupported file type for file '{file_path}'. Supported types: .pcap, .pcapng, .csv, .txt")
        sys.exit(1)

    if file_type == 'pcap':
        result = pcap_parser.parse_pcap(file_path)
    elif file_type == 'csv':
        result = csv_parser.parse_csv(file_path)
    elif file_type == 'txt':
        result = txt_parser.parse_txt(file_path)
    else:
        print("Error: Unknown file type detected.")
        sys.exit(1)

    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'summary.json')

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=4)

    print(f"Parsing complete. Summary saved to {output_path}")

if __name__ == '__main__':
    main()
