#!/usr/bin/env python3
"""
Quick implementation script for weighted balancing.
This will show you exactly what needs to be changed.
"""

print("""
🎯 WEIGHTED BALANCING IMPLEMENTATION
====================================

Follow these steps to add weighted load balancing:

STEP 1: Add to your .env file
------------------------------
Copy and paste this at the bottom of your .env file:

USE_WEIGHTED_BALANCING=true
GROQ_WEIGHT=30
OPENAI_WEIGHT=35
GEMINI_WEIGHT=35
ANTHROPIC_WEIGHT=30


STEP 2: Update multi_agent_ai.py
---------------------------------

2a) In __init__() method (line ~457), ADD after 'self.max_packets_per_chunk = 5000':

        # Load provider weights
        self.use_weighted_balancing = os.getenv("USE_WEIGHTED_BALANCING", "true").lower() == "true"
        self.provider_weights = {
            "Groq": float(os.getenv("GROQ_WEIGHT", "30")),
            "OpenAI": float(os.getenv("OPENAI_WEIGHT", "35")),
            "Google Gemini": float(os.getenv("GEMINI_WEIGHT", "35")),
            "Anthropic": float(os.getenv("ANTHROPIC_WEIGHT", "30"))
        }
        self.provider_usage_count = {}


2b) In __init__() method (line ~470), ADD after logger.info:

        if self.use_weighted_balancing:
            weights_str = ", ".join([f"{p.name}: {self.provider_weights.get(p.name, 33)}%" for p in self.active_providers])
            logger.info(f"🎯 Weighted balancing enabled: {weights_str}")


2c) REPLACE _select_provider() method (line ~640) with:

def _select_provider(self, chunk: Optional[PacketChunk] = None) -> Optional[AIProvider]:
    if not self.active_providers:
        return None
    
    if not self.use_weighted_balancing:
        provider = self.active_providers[0]
        self.active_providers.append(self.active_providers.pop(0))
        return provider
    
    for provider in self.active_providers:
        if provider.name not in self.provider_usage_count:
            self.provider_usage_count[provider.name] = 0
    
    adjusted_weights = []
    total_usage = sum(self.provider_usage_count.values()) or 1
    
    for provider in self.active_providers:
        target_ratio = self.provider_weights.get(provider.name, 33) / 100.0
        current_ratio = self.provider_usage_count.get(provider.name, 0) / total_usage
        adjustment = max(0.1, target_ratio - current_ratio + 0.5)
        adjusted_weights.append(adjustment * self.provider_weights.get(provider.name, 33))
    
    total_adjusted = sum(adjusted_weights)
    probabilities = [w / total_adjusted for w in adjusted_weights]
    selected_provider = random.choices(self.active_providers, weights=probabilities, k=1)[0]
    self.provider_usage_count[selected_provider.name] = self.provider_usage_count.get(selected_provider.name, 0) + 1
    
    return selected_provider


2d) In query_single_chunk() (line ~655), CHANGE:
    provider = self._select_provider()
TO:
    provider = self._select_provider(chunk)


STEP 3: Rebuild Docker
-----------------------
docker-compose down
docker-compose up -d --build


STEP 4: Verify
--------------
docker-compose logs | Select-String "Weighted"

You should see: "🎯 Weighted balancing enabled: Groq: 30%, OpenAI: 35%, Google Gemini: 35%"


DONE! 🎉
========

See WEIGHTED_BALANCING_GUIDE.md for detailed documentation.

""")
