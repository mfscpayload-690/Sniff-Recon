# Security Policy

## Supported Versions

We actively support the following versions of Sniff Recon with security updates:

| Version | Supported          | Status                     |
| ------- | ------------------ | -------------------------- |
| 2.0.x   | :white_check_mark: | **Current development**    |
| 1.0.x   | :white_check_mark: | Security fixes only        |
| < 1.0   | :x:                | No longer supported        |

**Current stable release:** v1.0.0 (August 10, 2024)  
**Development version:** v2.0.0 (in progress - see [ROADMAP.md](ROADMAP.md))

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Sniff Recon, please help us protect users by reporting it responsibly.

### 🔒 Private Disclosure Process

**DO NOT create a public GitHub issue for security vulnerabilities.**

Instead, please use one of these methods:

1. **GitHub Security Advisories** (Preferred):
   - Go to the [Security tab](https://github.com/mfscpayload-690/Sniff-Recon/security/advisories)
   - Click "Report a vulnerability"
   - Fill out the private advisory form

2. **Email** (Alternative):
   - Send details to: **[Create a GitHub issue for contact info request]**
   - Use subject: `[SECURITY] Sniff Recon Vulnerability Report`
   - Include PGP encryption if you have sensitive details

### What to Include

To help us understand and fix the issue quickly, please include:

- **Vulnerability type** (e.g., RCE, XSS, path traversal, DoS)
- **Affected component** (parser, AI module, UI, Docker, etc.)
- **Attack scenario**: How could this be exploited?
- **Proof of Concept** (PoC): Steps to reproduce or code snippet
- **Impact assessment**: What damage could an attacker cause?
- **Affected versions**: Which versions are vulnerable?
- **Suggested fix** (optional): How might we patch this?

### Response Timeline

We aim to respond to security reports within:

- **48 hours**: Initial acknowledgment of your report
- **7 days**: Preliminary assessment and severity classification
- **30 days**: Patch development and testing (for critical issues)
- **60 days**: Public disclosure after patch release (coordinated with you)

### Severity Classification

We use CVSS 3.1 scoring to classify vulnerabilities:

| Severity | CVSS Score | Response Time      |
| -------- | ---------- | ------------------ |
| Critical | 9.0-10.0   | Immediate (< 7 days) |
| High     | 7.0-8.9    | < 30 days          |
| Medium   | 4.0-6.9    | < 60 days          |
| Low      | 0.1-3.9    | Next release       |

## Security Considerations for Users

### Known Security Limitations

⚠️ **Sniff Recon is a network analysis tool, not a security product.** Please be aware:

1. **PCAP File Risks**:
   - PCAP files can contain malicious payloads (malware samples, exploit code)
   - **Never open untrusted PCAP files** on production systems
   - Use sandboxed environments (Docker, VMs) for analysis

2. **AI Provider Risks**:
   - Packet data is sent to AI providers (Groq, OpenAI, Anthropic) for analysis
   - **Do not analyze sensitive network traffic** with AI features enabled
   - Packet data may be logged by AI providers (check their privacy policies)
   - Use local analysis only (`--no-ai` mode) for confidential captures

3. **Memory Exhaustion**:
   - Large PCAP files (>200MB) are loaded into memory by Scapy
   - **Denial of Service risk**: Maliciously crafted large files can crash the app
   - GUI enforces 200MB limit, but CLI usage has no protection

4. **Code Injection via Parsers**:
   - CSV parser uses `pandas.read_csv()` which could execute formulas in Excel
   - **Never export parsed data to Excel** without sanitizing formulas
   - TXT parser uses `eval()` for packet reconstruction (potential RCE)

5. **Streamlit Session State**:
   - Packet data may persist in browser session storage
   - **Clear browser cache** after analyzing sensitive captures

### Recommended Safe Usage Practices

✅ **DO:**
- Run Sniff Recon in Docker containers (isolates file system access)
- Use virtual environments for Python installation
- Regularly update dependencies: `pip install -r requirements.txt --upgrade`
- Validate PCAP file integrity before analysis (`scapy.rdpcap()` error handling)
- Disable AI features when analyzing confidential traffic
- Review AI provider privacy policies before use

❌ **DON'T:**
- Analyze malware captures without sandboxing
- Run as root/administrator unless necessary
- Store AI API keys in code (use `.env` files, not committed to git)
- Trust packet data without validation (could be spoofed/crafted)
- Expose Streamlit app to public internet without authentication

## Security Features

### Current Protections

- **File size limits**: GUI enforces 200MB max for PCAP uploads
- **Input validation**: Parsers handle malformed files gracefully (return empty DataFrames)
- **Error isolation**: AI failures don't crash the app (fallback to local analysis)
- **Docker isolation**: Container runs with limited filesystem access
- **Dependency pinning**: `requirements.txt` locks package versions

### Planned Security Enhancements (v2.0.0+)

See [ROADMAP.md](ROADMAP.md) for:
- [ ] Authentication for multi-user deployments
- [ ] Encrypted storage for sensitive captures
- [ ] Audit logging for AI queries
- [ ] Rate limiting for API calls
- [ ] Content Security Policy (CSP) headers for Streamlit

## Dependencies Security

We monitor dependencies for known vulnerabilities using:

- **GitHub Dependabot**: Automated security updates
- **Manual reviews**: Quarterly dependency audits
- **Pinned versions**: `requirements.txt` specifies exact versions

### Reporting Dependency Vulnerabilities

If you find a vulnerable dependency:

1. Check if an update is available: `pip list --outdated`
2. Create a pull request with updated `requirements.txt`
3. Test that the update doesn't break functionality
4. Mention the CVE in PR description

## Third-Party Services

Sniff Recon integrates with external AI providers. **You are responsible for**:

- Reviewing their security/privacy policies
- Managing API keys securely (use environment variables)
- Understanding data retention policies
- Complying with your organization's data handling requirements

### AI Provider Security Policies

- **Groq**: [Groq Security](https://groq.com/security)
- **OpenAI**: [OpenAI Security](https://openai.com/security)
- **Anthropic**: [Anthropic Security](https://www.anthropic.com/security)

## Disclosure Policy

When a vulnerability is patched:

1. **Private fix**: We develop and test the patch privately
2. **Coordinated disclosure**: We notify the reporter before public release
3. **Security advisory**: We publish a GitHub Security Advisory
4. **Release notes**: We document the fix in `RELEASE_NOTES_vX.X.X.md`
5. **CVE request**: For critical issues, we request a CVE identifier
6. **Public disclosure**: After 90 days (or sooner with reporter's consent)

## Security Hall of Fame

We recognize security researchers who help make Sniff Recon safer:

<!-- No vulnerabilities reported yet - be the first! -->

*No security reports yet. If you find a vulnerability, you'll be listed here with your consent.*

## Legal Safe Harbor

We support security research conducted in good faith:

- **No legal action** will be taken against researchers who:
  - Report vulnerabilities privately per this policy
  - Avoid privacy violations and data destruction
  - Act in good faith without malicious intent

- **We will not pursue legal action** for:
  - Security testing on your own Sniff Recon installations
  - Responsible disclosure following this policy

## Contact

For security questions (non-vulnerability):
- Open a [GitHub Discussion](https://github.com/mfscpayload-690/Sniff-Recon/discussions)
- Create a public issue for security feature requests

For vulnerability reports:
- Use [GitHub Security Advisories](https://github.com/mfscpayload-690/Sniff-Recon/security/advisories) (private)

---

**Last Updated:** November 7, 2025  
**Policy Version:** 1.0  

*This security policy may be updated periodically. Check this file for the latest version.*
