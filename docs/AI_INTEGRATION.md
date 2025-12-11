# AI Integration Guide for CBT

## Overview

CBT now includes AI-powered features for intelligent attack coordination, adaptive evasion, and automated target analysis.

## AI Modules

### 1. AI Coordinator (`core/ai/coordinator.py`)

Intelligent attack orchestration that learns from previous attacks and adapts strategies.

**Features:**
- Target analysis and attack strategy selection
- Multi-phase attack planning
- Success rate learning and adaptation
- Optimal botnet selection

**Usage:**
```python
from core.ai.coordinator import AICoordinator

coordinator = AICoordinator(ufonet)
plan = coordinator.generate_attack_plan(target)
```

### 2. AI Evasion (`core/ai/evasion.py`)

Advanced evasion techniques to bypass WAFs and security measures.

**Features:**
- URL obfuscation
- Header randomization
- Request fragmentation
- Adaptive timing
- Protocol mixing
- WAF detection learning

**Usage:**
```python
from core.ai.evasion import AIEvasion

evasion = AIEvasion(ufonet)
evaded_request = evasion.evade_waf(request_data)
```

## CLI Integration

### AI-Powered Attack
```bash
./ufonet -a http://target.com --ai-coordinate
```

### AI Evasion Mode
```bash
./ufonet -a http://target.com --ai-evade
```

### AI Analysis
```bash
./ufonet --ai-analyze http://target.com
```

## How It Works

1. **Target Analysis**: AI analyzes target characteristics (protocol, response times, etc.)
2. **Strategy Selection**: Based on analysis, selects optimal attack vectors
3. **Adaptive Learning**: Learns from attack results and adjusts strategy
4. **Evasion**: Automatically applies evasion techniques when blocks detected

## Configuration

AI features can be configured in `core/ai/config.json`:
```json
{
  "learning_enabled": true,
  "evasion_aggressiveness": "medium",
  "adaptation_rate": 0.1,
  "history_size": 1000
}
```
