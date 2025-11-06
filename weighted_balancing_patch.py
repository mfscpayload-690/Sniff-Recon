"""
Weighted Balancing Patch for multi_agent_ai.py

This file contains the code changes needed to implement weighted provider balancing.

CHANGES REQUIRED:

1. In MultiAgentAI.__init__() - ADD these lines after self.max_packets_per_chunk:

        # Load provider weights from environment
        self.use_weighted_balancing = os.getenv("USE_WEIGHTED_BALANCING", "true").lower() == "true"
        self.provider_weights = {
            "Groq": float(os.getenv("GROQ_WEIGHT", "30")),  # Fast, good for quick scans
            "OpenAI": float(os.getenv("OPENAI_WEIGHT", "35")),  # Best quality
            "Google Gemini": float(os.getenv("GEMINI_WEIGHT", "35")),  # Large context
            "Anthropic": float(os.getenv("ANTHROPIC_WEIGHT", "30"))  # Premium quality
        }
        self.provider_usage_count = {}  # Track usage for balancing

2. In MultiAgentAI.__init__() - ADD at the end (after logger.info):

        if self.use_weighted_balancing:
            weights_str = ", ".join([f"{p.name}: {self.provider_weights.get(p.name, 33)}%" for p in self.active_providers])
            logger.info(f"🎯 Weighted balancing enabled: {weights_str}")
        else:
            logger.info("🔄 Using round-robin load balancing")

3. REPLACE the _select_provider() method with this:

    def _select_provider(self, chunk: Optional[PacketChunk] = None) -> Optional[AIProvider]:
        \"\"\"Select the best available provider using weighted balancing\"\"\"
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
        
        return selected_provider

4. UPDATE query_single_chunk() to pass chunk to _select_provider():

    async def query_single_chunk(self, prompt: str, chunk: PacketChunk) -> AIResponse:
        \"\"\"Query AI for a single packet chunk\"\"\"
        provider = self._select_provider(chunk)  # <-- ADD chunk parameter
        if not provider:
            return AIResponse(
                success=False,
                response="",
                error="No active AI providers available",
                chunk_id=chunk.chunk_id
            )
        
        # ... rest of method unchanged

5. ADD to .env.template:

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

\"\"\"
