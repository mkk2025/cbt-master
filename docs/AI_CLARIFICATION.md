# AI Integration - API Key Clarification

## Current AI Implementation

The AI features in CBT are **rule-based and statistical** - they do **NOT require any API keys**.

### How It Works

1. **AI Coordinator** (`core/ai/coordinator.py`)
   - Uses statistical analysis of attack history
   - Rule-based decision making
   - No external APIs needed
   - Works completely offline

2. **AI Evasion** (`core/ai/evasion.py`)
   - Pattern-based evasion techniques
   - Header randomization algorithms
   - Timing calculations
   - No external APIs needed

### No API Keys Required ✅

The current implementation is:
- **Self-contained** - All logic is in the code
- **Offline-capable** - Works without internet
- **Free** - No costs or API limits
- **Private** - No data sent to external services

## Optional: Enhanced AI with External APIs

If you want **more advanced AI capabilities**, you can optionally integrate:

### 1. OpenAI API (Optional)
- **Purpose**: Natural language processing, advanced pattern recognition
- **Use Cases**: 
  - Target content analysis
  - Social engineering payloads
  - Advanced evasion strategies
- **Cost**: Pay-per-use (requires API key)
- **Setup**: `export OPENAI_API_KEY="your-key"`

### 2. Anthropic Claude API (Optional)
- **Purpose**: Similar to OpenAI, alternative provider
- **Cost**: Pay-per-use
- **Setup**: `export ANTHROPIC_API_KEY="your-key"`

### 3. Local ML Models (Optional)
- **Purpose**: Machine learning for attack optimization
- **Libraries**: PyTorch, TensorFlow
- **Cost**: Free (runs locally)
- **Setup**: `pip3 install torch scikit-learn`

## Recommendation

**For most users**: The built-in rule-based AI is sufficient and requires no setup.

**For advanced users**: You can optionally add:
- Local ML models (free, runs offline)
- External AI APIs (paid, requires keys)

## Current AI Features (No Keys Needed)

✅ Target analysis and attack selection
✅ Success rate learning
✅ Adaptive evasion techniques
✅ Multi-phase attack planning
✅ WAF bypass strategies

All of these work **without any API keys**!
