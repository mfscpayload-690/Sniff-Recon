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
All parsers must return **pandas DataFrames** with standardized columns. Each parser is a simple function (no classes):

```python
# parsers/pcap_parser.py
def parse_pcap(file_path: str) -> pd.DataFrame:
    packets = rdpcap(file_path)  # Loads entire file into memory!
    # Returns: Timestamp, Source IP, Destination IP, Protocol, Source Port, Destination Port
```

**Critical Memory Pattern**: PCAP parser uses `scapy.rdpcap()` which loads entire file into memory. For large files (>200MB), the GUI enforces size limits at `sniff_recon_gui.py:179`.

**CSV Flexibility**: CSV parser handles inconsistent column names via key mapping (see `sniff_recon_gui.py` where file type detection occurs in file uploader section).

### 3. Streamlit State Management & Rerun Patterns
**Session State Keys** (`ai_query_interface.py:190-191`):
- `ai_responses`: List of all AI query results with timestamp (never cleared except on "Clear History")
- `user_query`: Pre-filled query text from suggested queries

**Critical Rerun Pattern** to avoid infinite loops:
```python
st.session_state.user_query = query  # Set state
st.rerun()  # Force UI refresh

# Later: ALWAYS clear before next rerun
st.session_state.user_query = ""
st.rerun()
```

**Never store packet data in session state** - packets are parsed fresh on each file upload and passed as function arguments.

### 4. CSS Injection Pattern
Every UI module calls `inject_modern_css()` or `inject_ai_interface_css()` to apply the cyberpunk-themed dark mode. **Always preserve CSS `unsafe_allow_html=True` patterns** when modifying UI. Pattern used throughout:

```python
st.markdown('<div class="protocol-card">...</div>', unsafe_allow_html=True)
```

## Development Workflows

### Running the Application
```powershell
# Primary method - checks dependencies, sets up environment
python start_gui.py

# Direct Streamlit (if deps already installed)
streamlit run sniff_recon_gui.py

# Custom port or Docker
streamlit run sniff_recon_gui.py --server.port 8502
docker-compose up -d  # Runs on port 8501, mounts ./output and .env
```

### Setting Up AI Providers (Optional)
1. Create `.env` in project root: `GROQ_API_KEY=...`, `OPENAI_API_KEY=...`, `ANTHROPIC_API_KEY=...`
2. Multi-agent system auto-detects and tests providers on init (`_test_providers()` in `multi_agent_ai.py:init`)
3. **Fallback**: App works without AI - provides local statistical analysis via `_provide_fallback_analysis()`

### Testing Packet Analysis
```python
# Parser testing (returns DataFrame)
from parsers.pcap_parser import parse_pcap
df = parse_pcap("test.pcap")

# AI analysis testing (returns Scapy packets)
import scapy.all as scapy
packets = scapy.rdpcap("test.pcap")  # For ai_module.query_ai()
```

## Project-Specific Conventions

### Error Handling Philosophy
- **AI Failures**: Always provide fallback analysis (see `_provide_fallback_analysis()` in `ai_module.py:409`)
- **API Errors**: Log to console, show user-friendly Streamlit warnings (not exceptions)
- **File Parsing**: Return empty DataFrame on failure, never crash GUI
- **No User Interruption**: App gracefully degrades when AI unavailable

### Data Flow for AI Queries
```
User Query → ai_query_interface.py (Streamlit UI)
  ↓
ai_module.py → filter_suspicious_packets() [Layer 1: reduce by ~90%]
  ↓
cluster_packets_by_ip() [Group by (src, dst) tuple]
  ↓
summarize_clusters() [Generate stats for LLM context]
  ↓
multi_agent_ai.py → chunk_packets() → query_single_chunk() [Parallel API calls]
  ↓
combine_responses() → Display in Streamlit with timestamp
```

**Why Layered Filtering?** Large PCAPs (100k+ packets) exceed LLM context windows. The 3-stage process (filter suspicious → cluster → summarize) reduces input by ~90% while preserving security insights.

### Scapy Packet Access Patterns (Critical!)
```python
# ALWAYS check layer presence before access - Scapy crashes otherwise
if IP in pkt:
    src_ip = pkt[IP].src  # Safe
    
if TCP in pkt:
    flags = pkt[TCP].flags & 0x02  # Check SYN flag

# NEVER: pkt[IP].src without check - crashes if no IP layer
# This pattern appears in: ai_module.py:filter_suspicious_packets(), parsers/pcap_parser.py
```

### Custom JSON Serialization
Scapy's `EDecimal` type breaks `json.dump()`. Use `CustomJSONEncoder` (defined in `sniff_recon_gui.py:14-19`):
```python
json.dump(summary, f, indent=4, cls=CustomJSONEncoder)  # Converts EDecimal→float
```

## Integration Points

### Streamlit Tabs Pattern
```python
# Standard tab structure used in sniff_recon_gui.py:327
tab1, tab2, tab3 = st.tabs(["📊 Packet Analysis", "🤖 AI Analysis", "💾 Export"])
with tab1:
    display_packet_table(packets)  # From display_packet_table.py
with tab2:
    render_ai_quick_analysis(packets)  # Quick summary
    render_ai_query_interface(packets)  # Natural language queries
with tab3:
    # JSON export functionality
```

### AgGrid Table Configuration (`display_packet_table.py`)
Uses `st-aggrid` for interactive packet tables with strict requirements:
- **Dark theme required**: `theme="dark"` (matches cyberpunk aesthetic)
- Single row selection for packet inspection
- Filter/sort enabled on all columns
- Column widths auto-adjusted based on content

### Protocol Layer Rendering Pattern
Each protocol has dedicated render function in `display_packet_table.py`:
```python
# Functions: render_ethernet_layer(), render_ip_layer(), render_transport_layer(), 
# render_application_layer(), render_packet_payload()
# Always wrap in: <div class="protocol-card">...</div> for consistent styling
```

## Common Pitfalls & Solutions

### 1. Packet Parsing Failures
**Issue**: CSV files with inconsistent column names  
**Solution**: Use key mapping dict in `sniff_recon_gui.py` (around line 122-129):
```python
mapped_row = {
    "src_ip": row.get("src_ip") or row.get("Source IP") or row.get("source_ip"),
    "dst_ip": row.get("dst_ip") or row.get("Destination IP") or row.get("dest_ip"),
    # Handle multiple naming conventions (snake_case, Title Case, camelCase)
}
```

### 2. Large File Memory Issues
**Issue**: `rdpcap()` loads entire file into RAM  
**Solution**: 
- GUI enforces 200MB limit (`sniff_recon_gui.py:179`)
- For future streaming: Consider `PcapReader` iterator pattern (progress bar example at line 242)
- Memory profiling: Large files may cause OOM - validate size before loading

### 3. AI Context Window Limits
**Issue**: LLMs reject inputs >8K tokens (Groq) or 100K tokens (OpenAI)  
**Solution**: 
- Multi-agent chunking is automatic in `multi_agent_ai.py`
- Verify `_format_chunk_context()` truncates properly (top 5 IPs/10 patterns max)
- Suspicious packet filtering reduces payload by ~90% before AI processing

### 4. Streamlit Rerun Loops
**Issue**: Infinite reruns when setting `st.session_state` in callbacks  
**Solution**: Always clear temporary state **before** `st.rerun()`:
```python
# Pattern from ai_query_interface.py:225-226, 290-291
st.session_state.user_query = query  # Set pre-filled query
st.rerun()  # Trigger refresh

# After query submission (lines 290-291):
st.session_state.user_query = ""  # CLEAR before rerun
st.rerun()  # Otherwise loops forever
```

### 5. Scapy Layer Access Crashes
**Issue**: Accessing `pkt[IP].src` without checking layer presence crashes with `IndexError`  
**Solution**: Defensive layer checking (see `ai_module.py:63-88`):
```python
if IP not in pkt:
    continue  # Skip non-IP packets (ARP, broadcasts, etc.)
# NOW safe to access pkt[IP].src
```

## File Organization Logic

- **`parsers/`**: Input format handlers (PCAP, CSV, TXT) → Return DataFrames
- **`utils/`**: Shared helpers (protocol name mapping via `get_protocol_name()`)
- **`output/`**: Runtime-generated JSON summaries (gitignored, created on startup)
- **Root UI files**: `sniff_recon_gui.py` (main entry), `display_packet_table.py` (AgGrid tables), `ai_query_interface.py` (AI chat UI)
- **AI files**: `multi_agent_ai.py` (primary multi-provider), `ai_module.py` (fallback + `PacketSummary` dataclass + filtering logic)
- **Startup**: `start_gui.py` (dependency checker + launcher), `run_gui.sh` (bash wrapper for venv)

## Testing & Debugging

### Quick Smoke Test
```powershell
# Test dependencies and launch
python start_gui.py  # Checks imports, starts Streamlit

# Test parser in isolation
python
>>> from parsers.pcap_parser import parse_pcap
>>> df = parse_pcap("sample.pcap")
>>> print(df.columns)  # Should show: Timestamp, Source IP, Destination IP, Protocol, etc.
```

### AI Provider Debugging
```python
# Check which providers are active
from multi_agent_ai import get_active_providers
providers = get_active_providers()  # Returns list of connected provider names

# Test single provider connection
from multi_agent_ai import GroqProvider
provider = GroqProvider(api_key="...")
is_connected = provider.test_connection()  # Returns bool
```

### Streamlit Debug Mode
Add to top of `sniff_recon_gui.py` for verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # Shows all Streamlit + Scapy internals
```

### Docker Debugging
```powershell
# View real-time logs
docker-compose logs -f

# Execute commands inside container
docker-compose exec sniff-recon bash
python -c "from parsers.pcap_parser import parse_pcap; print('OK')"

# Check health status
docker inspect sniff-recon | findstr Health
```

## Key Dependencies & Version Constraints
- **Scapy 2.5.0+**: Core packet parsing (uses `rdpcap`, `PcapReader`)
- **Streamlit 1.25.0+**: GUI framework (requires `st.file_uploader`, `st.tabs`)
- **st-aggrid 1.0.5+**: Interactive tables (dark theme support)
- **aiohttp 3.9.1+**: Async AI queries (multi-agent system)
- **PyShark 0.6.0+**: Alternative PCAP parser (currently unused, legacy dep)

## When Adding New Features

### New Parser Format
1. Create `parsers/new_format_parser.py` with function returning DataFrame
2. Add to `sniff_recon_gui.py` file type list (around line 174: `type=["pcap", "pcapng", "csv", "txt"]`)
3. Add parsing logic in file uploader section (line 184+ in try/except block)
4. Ensure DataFrame has standard columns: `Timestamp`, `Source IP`, `Destination IP`, `Protocol`, `Source Port`, `Destination Port`

### New AI Provider
1. Subclass `AIProvider` in `multi_agent_ai.py` (see `GroqProvider`, `OpenAIProvider` examples)
2. Implement required methods:
   - `__init__(api_key, model_name)`: Setup headers, endpoints
   - `async query(prompt, context)`: Return `AIResponse` with success/error
   - `test_connection()`: Return bool (ping API to validate key)
   - `@property name`: Return string provider name
   - `@property max_tokens`: Return int context window size
3. Add to `_initialize_providers()` in `MultiAgentAI` class with env var check:
```python
if os.getenv("NEW_PROVIDER_API_KEY"):
    self.providers.append(NewProvider(os.getenv("NEW_PROVIDER_API_KEY")))
```

### New Suspicious Pattern Detection
Add rules to `filter_suspicious_packets()` in `ai_module.py` (line 60+):
```python
# Check layer presence first (critical!)
if TCP in pkt:
    if pkt[TCP].flags & 0x04:  # RST flag example
        is_suspicious = True

# Add to bad_ports set for port-based detection
bad_ports = {0, 65535, 31337, 6667, 1337}  # Add your suspicious ports
```

### New Streamlit Tab
Add to tab list in `sniff_recon_gui.py:327`:
```python
tab1, tab2, tab3, tab4 = st.tabs(["📊 Packet Analysis", "🤖 AI Analysis", "💾 Export", "🔧 New Tab"])
with tab4:
    st.markdown('<div class="protocol-card">New Feature</div>', unsafe_allow_html=True)
    # Your logic here
```

---

**Last Updated**: 2025-11-06  
**Codebase Version**: v1.0.0 (Streamlit GUI Edition)
**Contributors**: Refer to GitHub commit history
