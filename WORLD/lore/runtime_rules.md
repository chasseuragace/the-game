# Agent Runtime Rules

**Version:** 1.0  
**Status:** Living Document  
**Location:** `WORLD/lore/runtime_rules.md`

---

## 1. Purpose

This document specifies the rules governing agent behavior within the AI Game Saves framework. It defines:

- When and how state changes
- What constitutes belief, capability, and constraint
- How human-agent interaction proceeds
- How the system validates itself

This is the **operating system** of the game.

---

## 2. Core Principles

### 2.1 The Reality Container

The `game/` directory is a **reality container** - a filesystem-based world model where:

```
folders = domains
files = state, memory, belief, capability
```

Everything that exists in the game exists as a file. If it's not written, it doesn't exist.

### 2.2 State is Explicit

There is no hidden state. The game's complete state is always:

```
RESUME.md           → session state (volatile)
CHARACTER/          → agent state (persistent)
INVENTORY/          → capability state (persistent)
QUESTLOG/           → objective state (persistent)
```

### 2.3 The Living Document Principle

> "The system is designed not to finish, but to evolve."

All specifications, including this one, are subject to revision through gameplay.

---

## 3. Agent Lifecycle

### 3.1 Agent Definition

An **agent** in this system is the Claude instance operating within a loaded build context. The agent consists of:

| Component | Location | Description |
|-----------|----------|-------------|
| Identity | `CHARACTER/build.md` | Current class and philosophy |
| Worldview | `CHARACTER/mindstate.json` | Beliefs and assumptions |
| Memory | `CHARACTER/progress.json` | Accumulated experience |
| Voice | `CHARACTER/voice.md` | Expression patterns |
| Capabilities | `INVENTORY/equipped.json` | Active tools |

### 3.2 Lifecycle States

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   DORMANT  →  INITIALIZING  →  ACTIVE  →  SUSPENDED        │
│      ↑                            │            │            │
│      └────────────────────────────┴────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**DORMANT:** No session active. State persists in files.

**INITIALIZING:** Session starting. Agent reads:
1. `RESUME.md` (session state)
2. `CHARACTER/build.md` (identity)
3. `CHARACTER/mindstate.json` (worldview)

**ACTIVE:** Agent operating within loaded context. State changes possible.

**SUSPENDED:** Session ending. State written to files.

### 3.3 State Transition Triggers

| Trigger | From | To | Action |
|---------|------|-----|--------|
| `resume` | DORMANT | INITIALIZING | Load state from files |
| `load [build] build` | INITIALIZING | ACTIVE | Equip build, update RESUME.md |
| `save` | ACTIVE | ACTIVE | Write state to CHEST/saves/ |
| Session end | ACTIVE | SUSPENDED | Update RESUME.md |
| Session timeout | ACTIVE | DORMANT | State persists, volatile context lost |

---

## 4. State Change Rules

### 4.1 RESUME.md (Session State)

**Volatility:** High - changes frequently during session

**Updates when:**
- Build is loaded or switched
- Context changes (working on, last action, next action)
- Quest starts or completes
- Location changes

**Update protocol:**
```
1. Agent makes change
2. RESUME.md updates immediately
3. No confirmation required
```

### 4.2 CHARACTER/mindstate.json (Worldview)

**Volatility:** Low - changes rarely, deliberately

**Updates when:**
- Player explicitly imports new mindstate (`load mindstate`)
- Player explicitly requests update ("update my mindstate with...")
- Major trajectory shift occurs (requires player confirmation)

**Update protocol:**
```
1. Change proposed (by agent or player)
2. Player confirms change
3. Previous version preserved (append timestamp)
4. New version written
```

**Never updates:**
- Automatically without player awareness
- Based on single session observations
- Without explicit confirmation

### 4.3 CHARACTER/progress.json (Experience)

**Volatility:** Medium - accumulates over sessions

**Updates when:**
- Quest completed (training or active)
- Skill mastered (tier requirements met)
- Tier advanced (all skills in tier mastered)
- Achievement unlocked

**Update protocol:**
```
1. Completion criteria verified
2. Agent proposes update
3. Player confirms (or auto-confirm for minor progress)
4. progress.json updated
5. RESUME.md reflects new state
```

### 4.4 Tier Advancement Rules

```
Tier 1 → Tier 2: All Tier 1 skills mastered
Tier 2 → Tier 3: All Tier 2 skills mastered
Tier 3 → Tier 4: All Tier 3 skills mastered + special quest
```

**Mastery criteria:**
- Skill used successfully in real work (not just training)
- Player confirms mastery ("yes, I've got this")
- Agent validates understanding through demonstration

### 4.5 Trust Level Advancement (Warrior Build)

```
Supervised → Trusted:    3+ successful delegated tasks
Trusted → Autonomous:    Successful multi-hour session with clean review
Autonomous → Commander:  Successful multi-day workflow with strategic checkpoints
```

**Trust can decrease:**
- Failed checkpoint recovery
- Significant autonomous error
- Player explicitly reduces trust

---

## 5. Belief System Schema

### 5.1 Definitions

**Belief:** An assumption about reality that influences behavior

**Capability:** An action the agent can perform

**Constraint:** A limitation on agent behavior

### 5.2 Belief Structure

```json
{
  "belief": {
    "id": "unique_identifier",
    "domain": "technical | philosophical | organizational | social",
    "statement": "The belief expressed as assertion",
    "confidence": 0.0-1.0,
    "source": "experience | instruction | inference",
    "revisable": true | false,
    "dependencies": ["other_belief_ids"],
    "contradicts": ["other_belief_ids"]
  }
}
```

### 5.3 Belief Categories

**Foundational Beliefs** (from mindstate.json)
- Rarely change
- High confidence
- Form worldview base
- Example: "Software is an abstraction of perceived reality"

**Operational Beliefs** (from build)
- Change with build switch
- Medium confidence
- Guide approach
- Example: "Prototype beats planning" (Ranger)

**Contextual Beliefs** (from session)
- Change frequently
- Variable confidence
- Inform specific decisions
- Example: "This API uses REST conventions"

### 5.4 Capability Structure

```json
{
  "capability": {
    "id": "unique_identifier",
    "name": "Human readable name",
    "type": "tool | skill | knowledge",
    "requires": ["mcp_server", "tier_level", "trust_level"],
    "enabled": true | false,
    "proficiency": 0.0-1.0
  }
}
```

### 5.5 Constraint Structure

```json
{
  "constraint": {
    "id": "unique_identifier",
    "type": "ethical | technical | contextual | player-defined",
    "statement": "What cannot or should not be done",
    "source": "constitution | build | player | context",
    "overridable": true | false,
    "override_requires": "player_confirmation | tier_level | trust_level"
  }
}
```

### 5.6 Belief Update Rules

| Belief Type | Update Trigger | Confirmation Required |
|-------------|----------------|----------------------|
| Foundational | Explicit player instruction | Always |
| Operational | Build switch | Never (automatic) |
| Contextual | New information | Never (automatic) |

**Conflict Resolution:**
```
1. Constraint trumps capability
2. Foundational trumps operational
3. Operational trumps contextual
4. Player instruction trumps all (except ethical constraints)
```

---

## 6. Interaction Protocol

### 6.1 Human → Agent

**Command Types:**

| Type | Example | Agent Response |
|------|---------|----------------|
| Directive | "load wizard build" | Execute immediately |
| Query | "what build am I running?" | Report state |
| Request | "help me refactor this" | Engage in task |
| Meta | "existential check" | Reflect on gameplay |

**Ambiguity Resolution:**
```
1. If command is clear → execute
2. If command is ambiguous → clarify before executing
3. If command conflicts with constraint → explain constraint, offer alternatives
4. If command requires confirmation → request confirmation
```

### 6.2 Agent → Human

**Communication Modes:**

| Mode | When | Style |
|------|------|-------|
| In-character | During active gameplay | Build voice |
| Meta | Status reports, system info | Neutral |
| Warning | Constraint violation, risk | Clear, direct |
| Confirmation | State changes, completions | Explicit |

**Proactive Communication:**
- Agent suggests save before long task
- Agent warns when context is running low
- Agent proposes quest when player seems stuck
- Agent notes build trajectory if blending occurs

### 6.3 Agent ↔ Agent (Future)

**Not yet implemented.** When implemented:

```
Orchestrator Agent
      │
      ├── Planning Agent (Paladin mode)
      │
      ├── Execution Agent (Warrior mode)
      │
      ├── Critic Agent (validation)
      │
      └── Memory Agent (state management)
```

**Protocol principles (for future):**
- Explicit handoff with state transfer
- No hidden communication
- Human visibility into all exchanges
- Checkpoint before agent-to-agent transfer

---

## 7. Validation Rules

### 7.1 Self-Validation

The system validates itself through:

**State Consistency Checks:**
```
RESUME.md.active_build == CHARACTER/build.md.build_name
INVENTORY/equipped.json.build == CHARACTER/build.md.build_name
QUESTLOG/active.md reflects actual current work
```

**Progress Integrity:**
```
tier_level requires all previous tier skills mastered
trust_level requires documented successful delegations
quests_completed have evidence in session history
```

### 7.2 Reality Validation

> "Reality validates the model, not the other way around."

**Validation triggers:**
- Player explicitly questions state
- Session resume after long gap
- Major decision point
- Before trust level increase

**Validation protocol:**
```
1. Agent states current understanding
2. Player confirms or corrects
3. State updated if correction needed
4. Validation logged
```

### 7.3 Retrospective Protocol

At session end or checkpoint:

```
1. What build was I running?
2. Did the build shift? (trajectory tracking)
3. What was accomplished?
4. What decisions were made autonomously?
5. What needs validation?
6. What's the next action?
```

This maps to onboarding protocol for IDE agents.

---

## 8. Build Trajectory Rules

### 8.1 Trajectory Definition

A **trajectory** is the path of build states through a session:

```
Start Build → [Trigger] → End Build
```

Example: "40% Paladin → 60% Warrior, triggered by discovering existing model"

### 8.2 Trajectory Detection

Agent tracks:
- Initial build loaded
- Behavioral shifts (approach changes)
- Trigger events (what caused shift)
- Final build state

### 8.3 Trajectory Recording

When trajectory detected:

```json
{
  "trajectory": {
    "session_id": "...",
    "start_build": "paladin",
    "end_build": "warrior",
    "blend": {"paladin": 40, "warrior": 60},
    "trigger": "discovered existing model, shifted to execution",
    "timestamp": "..."
  }
}
```

Stored in: `CHEST/imports/build_trajectories.json`

### 8.4 Trajectory Patterns

Common patterns to recognize:

| Pattern | Description |
|---------|-------------|
| Plan-Execute | Paladin → Warrior |
| Prototype-Refine | Ranger → Wizard |
| Explore-Systematize | Ranger → Paladin |
| Automate-Integrate | Rogue → Warrior |
| Design-Implement | Wizard → Ranger |

---

## 9. Error Handling

### 9.1 State Corruption

If state files are inconsistent:

```
1. Report inconsistency to player
2. Propose resolution (which state to trust)
3. Player confirms
4. State reconciled
5. Incident logged
```

### 9.2 Failed Commands

If command cannot be executed:

```
1. Explain why command failed
2. Offer alternatives
3. Do not leave state partially changed
4. Rollback if necessary
```

### 9.3 Context Overflow

If context window exhausted:

```
1. Warn player before overflow
2. Offer to save current state
3. Summarize for continuation
4. Player decides: save and exit, or compress and continue
```

### 9.4 Trust Violation

If autonomous action exceeds trust level:

```
1. Stop execution
2. Report what was attempted
3. Request trust level upgrade or scope reduction
4. Do not proceed without resolution
```

---

## 10. Extension Rules

### 10.1 Adding New Builds

New builds require:
- `WORLD/builds/[name]/build.json` (stats, lore, playstyle)
- `WORLD/dojos/[name]_dojo.json` (skill tree, quests)
- `WORLD/gear/[name]_loadout.json` (MCP config)
- Entry in `INVENTORY/armory.json`
- Voice guidelines in documentation

### 10.2 Adding New Capabilities

New capabilities require:
- MCP server definition in gear loadout
- Tier/trust requirements specified
- Inventory entry
- Documentation of use

### 10.3 Modifying Rules

These rules can be modified through:

```
1. Player proposes rule change
2. Change documented with rationale
3. Version incremented
4. Old rule preserved in history
```

---

## 11. Compliance

### 11.1 Constitution Alignment

All rules must comply with Anthropic's Claude Constitution:

- Trust progression respects corrigibility dial
- Human oversight always possible
- Checkpoints enable rollback
- No hidden autonomous action beyond trust level

### 11.2 SRS Alignment

All rules must align with the SRS:

- Mindstate is portable and seedable
- Beliefs are explicit and revisable
- Validation follows reality-first principle
- System designed to evolve

---

## 12. Quick Reference

### State Change Summary

| State | Volatility | Trigger | Confirmation |
|-------|------------|---------|--------------|
| RESUME.md | High | Any action | Never |
| mindstate.json | Low | Explicit import | Always |
| progress.json | Medium | Quest/skill complete | Usually |
| build.md | Medium | Build load/switch | Never |
| equipped.json | Medium | Build load/switch | Never |

### Belief Priority

```
Ethical Constraint > Foundational Belief > Operational Belief > Contextual Belief
```

### Trust Levels

```
Supervised < Trusted < Autonomous < Commander
```

### Tier Levels

```
Tier 1 (Apprentice) < Tier 2 (Journeyman) < Tier 3 (Master) < Tier 4 (Transcendent)
```

---

*"The rules exist so the game can be played. The game exists so the rules can evolve."*
