# Sniff Recon - AI Copilot Instructions

## Project Overview
Sniff Recon is a **Streamlit-based network packet analyzer** with AI-powered analysis capabilities. It parses PCAP, CSV, and TXT files to extract packet data and provides natural language querying through multiple AI providers (Groq, OpenAI, Anthropic).

**Key Architecture:** Streamlit GUI → Parser Layer → AI Module (Multi-Agent) → Scapy Packet Analysis

## Critical Architectural Patterns

### 1. Multi-Agent AI System (`multi_agent_ai.py`)
- **Chunking Strategy**: Large packet captures are split into 5MB/5000-packet chunks to avoid token limits
- **Load Balancing**: Round-robin across multiple AI providers (Groq, OpenAI, Anthropic)
- **Provider Abstraction**: All providers implement `AIProvider` abstract base class with `query()`, `test_connection()`, `name`, and `max_tokens` properties
- **Fallback Pattern**: If multi-agent fails, falls back to single Groq API via `ai_module.py`

```python
# Example: Multi-agent automatically chunks large files
chunks = multi_agent.chunk_packets(packets)  # Splits if >5MB or >5000 packets
responses = await multi_agent.query(prompt, packets)  # Processes chunks in parallel
```

### 2. Parser Layer Pattern (`parsers/`)
All parsers return **pandas DataFrames** with standardized columns:
- PCAP: `Timestamp`, `Source IP`, `Destination IP`, `Protocol`, `Source Port`, `Destination Port`
- CSV: Flexible mapping (see `sniff_recon_gui.py:122-129` for key normalization)
- TXT: Custom format handled by `txt_parser.py`

**Critical**: PCAP parser uses `scapy.rdpcap()` which loads entire file into memory. For large files (>200MB), the GUI enforces size limits.

### 3. Streamlit State Management
- **Session State Keys**:
  - `ai_responses`: List of all AI query results with timestamp
  - `user_query`: Current/pre-filled query text
  - Packet data is NOT stored in session state (passed fresh on rerun)

### 4. CSS Injection Pattern
Every UI module calls `inject_modern_css()` or `inject_ai_interface_css()` to apply the cyberpunk-themed dark mode. **Always preserve CSS `unsafe_allow_html=True` patterns** when modifying UI.

## Development Workflows

### Running the Application
```powershell
# Primary method (checks dependencies)
python start_gui.py

# Direct Streamlit (manual)
streamlit run sniff_recon_gui.py

# With custom port
streamlit run sniff_recon_gui.py --server.port 8502
```

### Setting Up AI Providers
1. Create `.env` file in project root
2. Add API keys: `GROQ_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
3. Multi-agent auto-detects and tests providers on init (`_test_providers()`)

### Testing Packet Analysis
```python
# Example workflow to test new parsers
from parsers.pcap_parser import parse_pcap
import scapy.all as scapy

df = parse_pcap("test.pcap")  # Returns DataFrame
packets = scapy.rdpcap("test.pcap")  # For AI analysis
```

## Project-Specific Conventions

### Error Handling
- **AI Failures**: Always provide fallback analysis (see `_provide_fallback_analysis()` in `ai_module.py`)
- **API Errors**: Log to console, show user-friendly Streamlit warnings (not exceptions)
- **File Parsing**: Return empty DataFrame on failure, never crash GUI

### Data Flow for AI Queries
```
User Query → ai_query_interface.py (Streamlit UI)
  ↓
ai_module.py → filter_suspicious_packets() [Layer 1 triage]
  ↓
cluster_packets_by_ip() [Group by (src, dst) tuple]
  ↓
summarize_clusters() [Generate stats for LLM]
  ↓
multi_agent_ai.py → chunk_packets() → query_single_chunk() [Parallel processing]
  ↓
combine_responses() → Display in Streamlit
```

**Why Layered Filtering?** Large PCAPs (100k+ packets) exceed LLM context windows. Suspicious packet filtering reduces input by ~90% while preserving security insights.

### Scapy Packet Access Patterns
```python
# ALWAYS check layer presence before access
if IP in pkt:
    src_ip = pkt[IP].src  # Safe
    
if TCP in pkt:
    flags = pkt[TCP].flags & 0x02  # Check SYN flag

# Avoid: pkt[IP].src (crashes if no IP layer)
```

### Custom JSON Serialization
Use `CustomJSONEncoder` (in `sniff_recon_gui.py`) for Scapy's `EDecimal` type when exporting to JSON:
```python
json.dump(summary, f, indent=4, cls=CustomJSONEncoder)
```

## Integration Points

### Streamlit Tabs Pattern
```python
tab1, tab2, tab3 = st.tabs(["📊 Packet Analysis", "🤖 AI Analysis", "💾 Export"])
with tab1:
    display_packet_table(packets)  # From display_packet_table.py
with tab2:
    render_ai_quick_analysis(packets)
    render_ai_query_interface(packets)
```

### AgGrid Table Configuration
`display_packet_table.py` uses `st-aggrid` for interactive packet tables. Key config:
- Dark theme required (`theme="dark"`)
- Single row selection for packet inspection
- Filter/sort enabled on all columns

### Protocol Layer Rendering
Each protocol has dedicated render function in `display_packet_table.py`:
- `render_ethernet_layer()`, `render_ip_layer()`, `render_transport_layer()`, etc.
- Always wrap in `<div class="protocol-card">` for consistent styling

## Common Pitfalls & Solutions

### 1. Packet Parsing Failures
**Issue**: CSV files with inconsistent column names  
**Solution**: Use key mapping dict (see `sniff_recon_gui.py:122-129`):
```python
mapped_row = {
    "src_ip": row.get("src_ip") or row.get("Source IP") or row.get("source_ip"),
    # ... handle multiple naming conventions
}
```

### 2. Large File Memory Issues
**Issue**: `rdpcap()` loads entire file into RAM  
**Solution**: 
- Enforce 200MB limit in GUI (`sniff_recon_gui.py:179`)
- For future: Consider `PcapReader` iterator for streaming (see progress bar example in `sniff_recon_gui.py:242`)

### 3. AI Context Window Limits
**Issue**: LLMs reject inputs >8K tokens  
**Solution**: Multi-agent chunking is automatic, but verify `_format_chunk_context()` doesn't exceed limits (currently truncates to top 5 IPs/10 patterns)

### 4. Streamlit Rerun Loops
**Issue**: Infinite reruns when setting `st.session_state` in callbacks  
**Solution**: Always clear temporary state before `st.rerun()`:
```python
st.session_state.user_query = ""
st.rerun()
```

## File Organization Logic

- **`parsers/`**: Input format handlers (PCAP, CSV, TXT) → Return DataFrames
- **`utils/`**: Shared helpers (protocol name mapping, etc.)
- **`output/`**: Runtime-generated JSON summaries (gitignored)
- **Root UI files**: `sniff_recon_gui.py` (main), `display_packet_table.py`, `ai_query_interface.py`
- **AI files**: `multi_agent_ai.py` (primary), `ai_module.py` (fallback + PacketSummary dataclass)

## Testing & Debugging

### Quick Smoke Test
```powershell
# Test dependencies
python start_gui.py  # Should check imports

# Test parser in isolation
python
>>> from parsers.pcap_parser import parse_pcap
>>> parse_pcap("sample.pcap")
```

### AI Provider Debugging
Check logs for provider status:
```python
from multi_agent_ai import get_active_providers
print(get_active_providers())  # Should list connected providers
```

### Streamlit Debug Mode
Add to `sniff_recon_gui.py` for verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Key Dependencies & Version Constraints
- **Scapy 2.5.0+**: Core packet parsing (uses `rdpcap`, `PcapReader`)
- **Streamlit 1.25.0+**: GUI framework (requires `st.file_uploader`, `st.tabs`)
- **st-aggrid 1.0.5+**: Interactive tables (dark theme support)
- **aiohttp 3.9.1+**: Async AI queries (multi-agent system)

## When Adding New Features

### New Parser Format
1. Create `parsers/new_format_parser.py` returning DataFrame
2. Add to `sniff_recon_gui.py` file type list (line 174)
3. Add parsing logic in try/except block (line 184+)

### New AI Provider
1. Subclass `AIProvider` in `multi_agent_ai.py`
2. Implement `query()`, `test_connection()`, `name`, `max_tokens`
3. Add to `_initialize_providers()` with env var check

### New Suspicious Pattern Detection
Add rules to `filter_suspicious_packets()` in `ai_module.py`:
- Check layer presence with `if TCP in pkt`
- Update `syn_counts` or `bad_ports` dicts
- Append to `is_suspicious` flag

---

**Last Updated**: 2025-11-05  
**Codebase Version**: v1.0.0 (Streamlit GUI Edition)
