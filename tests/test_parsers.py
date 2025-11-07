"""
Test suite for parser modules
"""
import pytest
from src.parsers import pcap_parser, csv_parser, txt_parser

def test_pcap_parser_exists():
    """Test that PCAP parser module exists"""
    assert hasattr(pcap_parser, 'parse_pcap')

def test_csv_parser_exists():
    """Test that CSV parser module exists"""
    assert hasattr(csv_parser, 'parse_csv')

def test_txt_parser_exists():
    """Test that TXT parser module exists"""
    assert hasattr(txt_parser, 'parse_txt')

# TODO: Add comprehensive parser tests with sample files
