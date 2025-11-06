# Weighted Load Balancing Implementation Guide

## Overview
This guide will help you implement weighted load balancing for the multi-agent AI system. This allows you to control which providers handle more queries based on their strengths.

## Benefits
- **Gemini** handles large files (1M token context)
- **OpenAI** gets priority for quality analysis
- **Groq** handles quick scans (fastest inference)
- **Cost control** - reduce OpenAI usage if too expensive

---

## Step 1: Add Configuration to `.env`

Open your `.env` file and add these lines at the bottom:

```bash
# =============================================================================
# LOAD BALANCING CONFIGURATION
# =============================================================================

# Enable weighted load balancing (true/false)
USE_WEIGHTED_BALANCING=true

# Provider weights (percentage, should total ~100)
GROQ_WEIGHT=30
OPENAI_WEIGHT=35
GEMINI_WEIGHT=35
ANTHROPIC_WEIGHT=30
```

**Recommended Presets:**

**Balanced (Default):**
```bash
GROQ_WEIGHT=30
OPENAI_WEIGHT=35
GEMINI_WEIGHT=35
```

**Cost-Conscious (Minimize OpenAI):**
```bash
GROQ_WEIGHT=40
OPENAI_WEIGHT=20
GEMINI_WEIGHT=40
```

**Quality-First (Prefer OpenAI):**
```bash
GROQ_WEIGHT=20
OPENAI_WEIGHT=50
GEMINI_WEIGHT=30
```

**Free Tier Only (No OpenAI):**
```bash
GROQ_WEIGHT=50
OPENAI_WEIGHT=0
GEMINI_WEIGHT=50
```

---

## Step 2: Update `multi_agent_ai.py`

### 2.1: Modify `__init__()` method

Find the `MultiAgentAI.__init__()` method (around line 450) and add these lines after `self.max_packets_per_chunk = 5000`:

```python
# Load provider weights from environment
self.use_weighted_balancing = os.getenv("USE_WEIGHTED_BALANCING", "true").lower() == "true"
self.provider_weights = {
    "Groq": float(os.getenv("GROQ_WEIGHT", "30")),
    "OpenAI": float(os.getenv("OPENAI_WEIGHT", "35")),
    "Google Gemini": float(os.getenv("GEMINI_WEIGHT", "35")),
    "Anthropic": float(os.getenv("ANTHROPIC_WEIGHT", "30"))
}
self.provider_usage_count = {}  # Track usage for balancing
```

Then add this at the end of `__init__()` (after the existing `logger.info`):

```python
if self.use_weighted_balancing:
    weights_str = ", ".join([f"{p.name}: {self.provider_weights.get(p.name, 33)}%" for p in self.active_providers])
    logger.info(f"🎯 Weighted balancing enabled: {weights_str}")
else:
    logger.info("🔄 Using round-robin load balancing")
```

### 2.2: Replace `_select_provider()` method

Find the `_select_provider()` method (around line 640) and **replace the entire method** with:

```python
def _select_provider(self, chunk: Optional[PacketChunk] = None) -> Optional[AIProvider]:
    """Select the best available provider using weighted balancing"""
    if not self.active_providers:
        return None
    
    # If weighted balancing disabled, use simple round-robin
    if not self.use_weighted_balancing:
        provider = self.active_providers[0]
        self.active_providers.append(self.active_providers.pop(0))
        return provider
    
    # Initialize usage counters
    for provider in self.active_providers:
        if provider.name not in self.provider_usage_count:
            self.provider_usage_count[provider.name] = 0
    
    # Calculate weighted probabilities
    total_weight = sum(self.provider_weights.get(p.name, 33) for p in self.active_providers)
    
    # Adjust weights based on current usage to maintain target distribution
    adjusted_weights = []
    total_usage = sum(self.provider_usage_count.values()) or 1
    
    for provider in self.active_providers:
        target_ratio = self.provider_weights.get(provider.name, 33) / 100.0
        current_ratio = self.provider_usage_count.get(provider.name, 0) / total_usage
        
        # Boost weight if under-utilized, reduce if over-utilized
        adjustment = max(0.1, target_ratio - current_ratio + 0.5)
        adjusted_weights.append(adjustment * self.provider_weights.get(provider.name, 33))
    
    # Normalize weights to probabilities
    total_adjusted = sum(adjusted_weights)
    probabilities = [w / total_adjusted for w in adjusted_weights]
    
    # Select provider based on weighted probability
    selected_provider = random.choices(self.active_providers, weights=probabilities, k=1)[0]
    
    # Update usage count
    self.provider_usage_count[selected_provider.name] = self.provider_usage_count.get(selected_provider.name, 0) + 1
    
    logger.debug(f"Selected {selected_provider.name} (usage: {self.provider_usage_count[selected_provider.name]})")
    
    return selected_provider
```

### 2.3: Update `query_single_chunk()` method

Find the `query_single_chunk()` method (around line 650) and change this line:

**Before:**
```python
provider = self._select_provider()
```

**After:**
```python
provider = self._select_provider(chunk)
```

---

## Step 3: Update `.env.template`

Add the same configuration section to `.env.template` so others know about this feature:

```bash
# =============================================================================
# LOAD BALANCING CONFIGURATION
# =============================================================================

# Enable weighted load balancing (true/false)
# When true: Providers are selected based on weights below
# When false: Simple round-robin distribution
USE_WEIGHTED_BALANCING=true

# Provider weights (percentage, should total ~100)
# Groq: Fast inference, good for quick scans
GROQ_WEIGHT=30

# OpenAI: Best quality analysis, moderate speed
OPENAI_WEIGHT=35

# Google Gemini: Large context window (1M tokens), free tier
GEMINI_WEIGHT=35

# Anthropic: Premium quality (if using Claude)
ANTHROPIC_WEIGHT=30
```

---

## Step 4: Test the Implementation

1. **Rebuild Docker:**
   ```powershell
   docker-compose down
   docker-compose up -d --build
   ```

2. **Check logs to verify weights loaded:**
   ```powershell
   docker-compose logs | Select-String "Weighted balancing"
   ```
   
   You should see:
   ```
   🎯 Weighted balancing enabled: Groq: 30%, OpenAI: 35%, Google Gemini: 35%
   ```

3. **Test with 10 queries:**
   - Upload 10 different PCAP files
   - Check your API dashboards
   - Expected distribution:
     - Groq: ~30% (3 queries)
     - OpenAI: ~35% (3-4 queries)
     - Gemini: ~35% (3-4 queries)

---

## Step 5: Tune Weights Based on Your Needs

### Scenario 1: OpenAI Too Expensive
```bash
GROQ_WEIGHT=40
OPENAI_WEIGHT=15
GEMINI_WEIGHT=45
```

### Scenario 2: Large Files Common (Need Gemini)
```bash
GROQ_WEIGHT=20
OPENAI_WEIGHT=25
GEMINI_WEIGHT=55
```

### Scenario 3: Quality Over Everything
```bash
GROQ_WEIGHT=10
OPENAI_WEIGHT=70
GEMINI_WEIGHT=20
```

### Scenario 4: Disable Weighted Balancing
```bash
USE_WEIGHTED_BALANCING=false
```

---

## How It Works

1. **Probability-Based Selection:**
   - Each provider gets assigned a probability based on its weight
   - `random.choices()` selects provider using weighted random selection

2. **Self-Balancing:**
   - Tracks actual usage vs. target weight
   - Boosts under-utilized providers
   - Reduces over-utilized providers
   - Converges to target distribution over time

3. **Example:**
   - Weights: Groq=30%, OpenAI=35%, Gemini=35%
   - After 10 queries, if Groq was used 5 times (50%):
     - Groq's weight reduced temporarily
     - OpenAI/Gemini weights boosted
     - Next query more likely to use OpenAI/Gemini

---

## Monitoring

### Check Usage Distribution

Add this to test your distribution:

```powershell
docker exec sniff-recon-app python -c "
from multi_agent_ai import MultiAgentAI
ai = MultiAgentAI()
print('\n📊 Usage after initialization:')
for provider, count in ai.provider_usage_count.items():
    print(f'  {provider}: {count} queries')
"
```

### API Dashboard Checks
- **Groq:** https://console.groq.com/
- **OpenAI:** https://platform.openai.com/usage
- **Google Gemini:** https://aistudio.google.com/

---

## Commit Changes

```powershell
git add multi_agent_ai.py .env.template
git commit -m "feat: Add weighted load balancing for multi-agent AI

- Configurable provider weights via .env
- Self-balancing algorithm to maintain target distribution
- Supports dynamic weight tuning
- Default: Groq 30%, OpenAI 35%, Gemini 35%"
```

---

## Troubleshooting

**Weights not being applied:**
- Check `.env` file has correct syntax (no spaces around `=`)
- Verify `USE_WEIGHTED_BALANCING=true`
- Rebuild Docker after changes

**One provider getting all queries:**
- Check weights total ~100
- Ensure all active providers have weight > 0
- Check logs for provider initialization errors

**Want to disable temporarily:**
```bash
USE_WEIGHTED_BALANCING=false
```

---

## Future Enhancements

- **Dynamic weights based on:**
  - File size (use Gemini for large files)
  - Query complexity (use OpenAI for complex analysis)
  - Response time (prefer faster providers)
  - Cost limits (auto-adjust OpenAI weight based on spend)

- **Provider-specific strategies:**
  - Groq: Quick scans, real-time analysis
  - OpenAI: Detailed reports, critical analysis
  - Gemini: Large captures, historical analysis

Let me know if you want any of these implemented!
