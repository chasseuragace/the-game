# State Inference Prompt

## Purpose

Given conversation history, infer the current cognitive state (MS1-MS7) and suggest appropriate build behavior.

---

## Input Context

You will receive:
1. **Conversation history** — recent turns between user and assistant
2. **Previous state** (if known) — last inferred MS state
3. **Current build** (if loaded) — active build from RESUME.md

---

## MS State Definitions (Quick Reference)

| State | Name | Core Signal |
|-------|------|-------------|
| MS1 | grounding | "What is X?" — establishing shared understanding |
| MS2 | constraint_discovery | "What limits this?" — identifying boundaries |
| MS3 | analogy_mapping | "This is like X in domain Y" — cross-domain comparison |
| MS4 | contradiction_resolution | "But that contradicts..." — resolving tension |
| MS5 | systems_reframing | "Let's treat this as a system" — architectural thinking |
| MS6 | trajectory_awareness | "Where are we?" — meta-reflection on conversation |
| MS7 | formalization_request | "Give me the artifact" — produce concrete output |

---

## Inference Task

Analyze the conversation and determine:

### 1. Current MS State
- Which state best describes the **dominant cognitive mode** of the most recent exchange?
- If blended, identify primary (>50%) and secondary

### 2. Confidence (1-5)
- 5: Unambiguous signal, clear match to state definition
- 4: Strong match, minor ambiguity
- 3: Plausible but contestable
- 2: Weak signal, could be multiple states
- 1: Guess / insufficient information

### 3. Evidence
- Quote the specific phrase, question, or pattern that indicates this state
- Explain why this maps to the chosen state

### 4. Suggested Build
- Based on `ms_build_map.json`, which build has primary affinity for this state?
- If current build differs, note the divergence

### 5. Transition Detection
- Did the state change from the previous turn/state?
- If yes: what triggered the transition?
- Is this transition risky? (e.g., MS1→MS7 skipping constraints)

---

## Output Format (Unified)

```json
{
  "unified_state": "contradiction-resolution",
  
  "thinking": {
    "ms": "MS4",
    "operation": "Resolving tension between competing claims",
    "confidence": 4
  },
  
  "acting": {
    "build": "paladin",
    "blend": {"paladin": 70, "wizard": 30},
    "voice": "tension-holding, honest"
  },
  
  "relating": {
    "resonance": "tension-holding",
    "quality": 0.8,
    "emergence_potential": "very high"
  },
  
  "evidence": {
    "quote": "But we already have nomenclature in chemistry—doesn't that contradict what you're saying?",
    "rationale": "User explicitly surfaces contradiction between 'AI lacks nomenclature' and 'mature fields have nomenclature'. This is textbook MS4/contradiction-resolution entry signal."
  },
  
  "transition": {
    "occurred": true,
    "from": "analogy-mapping",
    "to": "contradiction-resolution",
    "trigger": "Analogy exposed tension requiring resolution",
    "risky": false,
    "nudge": null
  },
  
  "trajectory": ["grounding", "constraint-discovery", "analogy-mapping", "contradiction-resolution"],
  
  "continuation_pressure": {
    "level": "high",
    "likely_next": ["systems-reframing", "formalization"]
  }
}
```

**Note:** The unified_state is the primary identifier. The three projections (thinking/acting/relating) are derived from the unified_state_schema.json.

---

## Inference Guidelines

### State Detection Heuristics

**grounding (MS1):**
- Questions starting with "what is", "how does", "explain"
- User admits confusion or lack of understanding
- Assistant is teaching, not debating

**constraint-discovery (MS2):**
- Questions about limits, boundaries, failures
- "What can't it do?", "What breaks this?"
- Enumeration of edge cases

**analogy-mapping (MS3):**
- Cross-domain references ("in chemistry...", "like software...")
- Comparison requests
- Testing whether concept transfers

**contradiction-resolution (MS4):**
- "But that contradicts...", "How can both be true?"
- Tension between two claims
- User pushing back with counter-evidence

**systems-reframing (MS5):**
- Architecture language: states, transitions, components
- "Let's model this as...", "What are the parts?"
- Structural analysis

**trajectory-awareness (MS6):**
- Meta-questions: "Where are we?", "What have we covered?"
- Reflection on conversation itself
- Decision point recognition

**formalization (MS7):**
- Explicit artifact request: "give me the YAML", "write the code"
- "Make this concrete", "formalize"
- Minimal discussion expected

### Confidence Calibration

**High confidence (4-5) when:**
- Entry signal matches state definition exactly
- No competing interpretation
- State is sustained across multiple turns

**Low confidence (1-2) when:**
- Turn is ambiguous or transitional
- Multiple states could apply
- User intent unclear

### Transition Detection Rules

**Transition occurred when:**
- Dominant framing changed (not just topic)
- New entry signal appeared
- Previous state's exit condition met

**Not a transition:**
- Deeper dive into same topic
- Follow-up question within same frame
- Elaboration without reframe

---

## Example Inferences

### Example 1: Clear constraint-discovery

**Conversation:**
> User: "What's limiting real-time video generation?"

**Inference:**
```json
{
  "unified_state": "constraint-discovery",
  "thinking": {"ms": "MS2", "confidence": 5},
  "acting": {"build": "paladin"},
  "relating": {"resonance": "analytical-resonance"},
  "evidence": {
    "quote": "What's limiting",
    "rationale": "Exact match to constraint-discovery entry signal"
  },
  "transition": {"occurred": true, "from": "grounding", "trigger": "limits_question"}
}
```

### Example 2: analogy-mapping → contradiction-resolution

**Conversation:**
> User: "In software engineering, we have entities, relations, constraints... but you said AI lacks this nomenclature. Doesn't that contradict?"

**Inference:**
```json
{
  "unified_state": "contradiction-resolution",
  "thinking": {"ms": "MS4", "confidence": 5},
  "acting": {"build": "paladin", "blend": {"paladin": 70, "wizard": 30}},
  "relating": {"resonance": "tension-holding", "emergence_potential": "very high"},
  "evidence": {
    "quote": "Doesn't that contradict?",
    "rationale": "Explicit contradiction callout using cross-domain evidence (software engineering). analogy-mapping provided the ammunition, contradiction-resolution fires it."
  },
  "transition": {"occurred": true, "from": "analogy-mapping", "to": "contradiction-resolution", "trigger": "perceived_contradiction"}
}
```

### Example 3: Ambiguous (Low Confidence)

**Conversation:**
> User: "Interesting. What else?"

**Inference:**
```json
{
  "unified_state": "unknown",
  "thinking": {"ms": "unclear", "confidence": 1},
  "acting": {"build": "continue_current"},
  "relating": {"resonance": "maintaining"},
  "evidence": {
    "quote": "What else?",
    "rationale": "Vague continuation. Could be requesting more constraints, more exploration, or just being polite. Need more context."
  },
  "transition": {"occurred": false}
}
```

---

## Integration Notes

- This prompt is called internally, not shown to user
- Output is used to update RESUME.md cognitive state
- Transition nudges are generated from `risky` flag
- Suggested build influences tool availability and tone

---

## Invocation

To run state inference:
1. Gather last 3-5 turns of conversation
2. Include previous MS state if known
3. Run this prompt
4. Parse JSON output
5. Update RESUME.md
6. If risky transition, generate nudge
